from fastapi import FastAPI, Depends, HTTPException, Request
from .models import Base, URL
from .database import engine, SessionLocal
from pydantic import BaseModel, Field
from typing import Annotated
from sqlalchemy.orm import Session
from .services import encode_base62
from fastapi.responses import RedirectResponse
from .redis_client import redis_client
from .rate_limiter import check_rate_limit
import socket
from prometheus_fastapi_instrumentator import Instrumentator
import time
from .logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()

Instrumentator().instrument(app).expose(app)


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    try:
        response = await call_next(request)

        process_time = round(time.time() - start_time, 3)

        logger.info(
            f"method={request.method} "
            f"path={request.url.path} "
            f"status={response.status_code} "
            f"duration={process_time}s"
        )

        return response

    except Exception as e:

        logger.exception(
            f"unhandled_exception path={request.url.path}"
        )

        raise



@app.get("/")
async def health():
    HOSTNAME = socket.gethostname()
    logger.info(
        f"hostname={HOSTNAME} "
        f"status=running"
    )
    return {
        "status": "running",
        "hostname": HOSTNAME
    }


class URLRequest(BaseModel):
    url: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/shorten")
async def shorten(request:Request, payload:URLRequest, db: db_dependency):
    url = URL(long_url=payload.url)

    ip = request.client.host #127.0.0.1
    check_rate_limit(ip)

    logger.info(
        f"url_creation_requested "
        f"ip={ip} "
        f"url={payload.url}"
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    short_code = encode_base62(url.id)

    logger.info(
        f"url_created "
        f"short_code={short_code}"
    )

    url.short_code = short_code

    db.commit()
    db.refresh(url)


    return {
        "short_url": f"http://localhost:8000/{url.short_code}"
    }


@app.get("/{short_code}")
async def shorten(short_code: str, db: db_dependency):

    cached_url = redis_client.get(short_code)
    if cached_url:
        logger.info(
            f"cache_hit short_code={short_code}"
        )
        logger.info(
            f"redirecting short_code={short_code}"
        )
        return RedirectResponse(url=cached_url)

    logger.info(
        f"cache_miss short_code={short_code}"
    )

    data = db.query(URL).filter(URL.short_code == short_code).first()

    if not data:
        logger.warning(
            f"url_not_found short_code={short_code}"
        )
        raise HTTPException(status_code=404,detail="URL not found")

    redis_client.set(short_code,data.long_url,ex=3600)

    logger.info(
        f"cache_populated short_code={short_code}"
    )
    logger.info(
        f"redirecting short_code={short_code}"
    )
    return RedirectResponse(url=data.long_url)
