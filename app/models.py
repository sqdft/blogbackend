from __future__ import annotations
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .db import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), index=True, nullable=False)
    nickname = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    ip = Column(String(64), nullable=True)
    ua = Column(String(256), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
