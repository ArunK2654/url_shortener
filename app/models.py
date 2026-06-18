from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True, nullable=False)
    short_code = Column(String(10), unique=True, index=True, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
