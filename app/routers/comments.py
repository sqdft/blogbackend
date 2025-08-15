from __future__ import annotations
import html
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from ..db import get_db, engine
from ..models import Comment
from ..schemas import CommentCreate, CommentRead, CommentsPage
from ..security import require_admin_token
from ..db import Base

# 确保表已创建（简单场景下可用；生产建议用迁移工具）
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api/comments", tags=["comments"])

MAX_PAGE_SIZE = 50

@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(payload: CommentCreate, request: Request, db: Session = Depends(get_db)):
    # 简单清洗与长度保护
    safe_nickname = html.escape(payload.nickname.strip())[:64]
    safe_content = html.escape(payload.content.strip())[:2000]
    safe_path = payload.path.strip()[:255]

    if not safe_nickname or not safe_content or not safe_path:
        raise HTTPException(status_code=400, detail="Invalid input")

    ip = request.client.host if request.client else None
    ua = request.headers.get("User-Agent")[:256] if request.headers.get("User-Agent") else None

    c = Comment(path=safe_path, nickname=safe_nickname, content=safe_content, ip=ip, ua=ua)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("", response_model=CommentsPage)
def list_comments(
    path: str = Query(..., min_length=1, max_length=255),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
):
    # 统计总数
    total = db.execute(select(func.count()).select_from(Comment).where(Comment.path == path)).scalar_one()

    # 分页
    offset = (page - 1) * page_size
    stmt = (
        select(Comment)
        .where(Comment.path == path)
        .order_by(Comment.created_at.desc(), Comment.id.desc())
        .offset(offset)
        .limit(page_size)
    )
    items = list(db.execute(stmt).scalars().all())

    return CommentsPage(items=items, total=total, page=page, page_size=page_size)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin_token)])
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    obj = db.get(Comment, comment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(obj)
    db.commit()
    return None
