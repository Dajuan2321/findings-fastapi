from fastapi import APIRouter
from app.schedule.crawler import NewsCrawler

router = APIRouter(
    prefix="/schedule"
)

@router.get("/posts")
async def posts():
    crawler = NewsCrawler()
    crawler.general()
    crawler.world()
    crawler.nation()
    crawler.business()
    crawler.technology()
    crawler.entertainment()
    crawler.sports()
    crawler.science()

    return "ok"