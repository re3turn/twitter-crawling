from fastapi import APIRouter

from ..models import entity
from ..cruds import twitter as curd_twitter
from typing import List


router = APIRouter()


@router.get("/users/{user_id}")
async def fetch_user_profile(user_id: str) -> entity.UserProfile:
    return await curd_twitter.fetch_user_profile(user_id)


@router.get("/users/{user_id}/tweets")
async def fetch_tweets(user_id: str, cursor: str = "", limit: int = 100) -> List[entity.ResponseItems]:
    tweets: entity.Tweet = await curd_twitter.fetch_tweets(user_id, cursor, limit)
    return entity.ResponseItems(tweets)


@router.get("/tweets/search")
async def fetch_tweets(query: str) -> List[entity.ResponseItems]:
    tweets: entity.Tweet = await curd_twitter.fetch_search_tweets(query)
    return entity.ResponseItems(tweets)


@router.get("/tweets/{tweet_id}")
async def fetch_tweets(tweet_id: str) -> entity.Tweet:
    return await curd_twitter.fetch_tweet(tweet_id)
