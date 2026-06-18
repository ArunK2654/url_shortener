from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


postgres_url = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/urlshortener"
)
engine = create_engine(postgres_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()