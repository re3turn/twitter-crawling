from fastapi import APIRouter
from src.routers.twitter import router as twitter_router


router = APIRouter()
router.include_router(twitter_router, prefix="/api", tags=["api"])
