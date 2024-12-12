from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.db.dao import PostsDao


router = APIRouter(
    prefix="/posts"
)

# Pydantic 模型用于验证请求和响应数据
class PostsItem(BaseModel):
    id: int
    xid: Optional[str]
    title: str
    thumbnail: Optional[str]
    description: Optional[str]
    url: str
    url_sid: Optional[str]
    source: Optional[str]
    publisher: Optional[str]
    category: Optional[str]
    views: int
    logo: Optional[str]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True

class PaginatedNewsResponse(BaseModel):
    items: List[PostsItem]
    total: int
    page: int
    size: int
    pages: int

@router.get("/list", response_model=PaginatedNewsResponse)
async def list(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=20),
        title: Optional[str] = Query(None, min_length=1),
        category: Optional[str] = Query(None, min_length=1),
):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Page and size must be positive integers")

    dao = PostsDao()

    page_data = dao.page(page, size, title, category)

    return PaginatedNewsResponse(
        items=page_data['items'],
        total=page_data['total'],
        page=page_data['page'],
        size=page_data['size'],
        pages=page_data['pages']
    )