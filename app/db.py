from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine.url import make_url
from .config import settings

if not settings.DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# 创建数据库引擎（将 psycopg2 驱动名自动迁移为 psycopg3）
_db_url = make_url(settings.DATABASE_URL)
if _db_url.drivername == "postgresql+psycopg2":
    _db_url = _db_url.set(drivername="postgresql+psycopg")
elif _db_url.drivername == "postgresql":
    # 强制使用 psycopg3 驱动，避免在不同环境下加载到旧驱动
    _db_url = _db_url.set(drivername="postgresql+psycopg")

engine = create_engine(_db_url, pool_pre_ping=True)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# 依赖：获取 DB 会话
from typing import Generator

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
