from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CommentCreate(BaseModel):
    path: str = Field(..., min_length=1, max_length=255)
    nickname: str = Field(..., min_length=1, max_length=64)
    content: str = Field(..., min_length=1, max_length=2000)

class CommentRead(BaseModel):
    id: int
    path: str
    nickname: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class CommentsPage(BaseModel):
    items: List[CommentRead]
    total: int
    page: int
    page_size: int
