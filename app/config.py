from __future__ import annotations
import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv

# 加载 backend/.env（本地开发），并强制覆盖已有环境变量，避免系统环境变量遮蔽
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    ADMIN_TOKEN: str = os.getenv("ADMIN_TOKEN", "")
    CORS_ORIGINS: List[str] = [s.strip() for s in os.getenv("CORS_ORIGINS", "*").split(",")] if os.getenv("CORS_ORIGINS") else ["*"]

settings = Settings()
