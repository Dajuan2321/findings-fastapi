from fastapi import APIRouter, Query, HTTPException
from app.db.dao import PostsDao

router = APIRouter(
    prefix="/live"
)

@router.get("/ping")
async def ping():
    return "pong"

@router.get("/mysql")
async def mysql():
    dao = PostsDao()

    return dao.get_posts(posts_id = 1) or {}