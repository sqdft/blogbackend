from __future__ import annotations
from fastapi import HTTPException, status, Header
from typing import Optional
from .config import settings

BEARER_PREFIX = "Bearer "

async def require_admin_token(authorization: Optional[str] = Header(default=None)) -> None:
    if not authorization or not authorization.startswith(BEARER_PREFIX):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")
    token = authorization[len(BEARER_PREFIX):].strip()
    if not settings.ADMIN_TOKEN or token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
