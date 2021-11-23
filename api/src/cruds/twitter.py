from typing import List, Optional

import motor.motor_asyncio
import pymongo

from ..models import entity
from ..utils.env import Env
from ..utils.util import get_dict_value

DATABASE_URL = Env.get_environment('DATABASE_URL', required=True)
DB_NAME = Env.get_environment('MONGO_DATABASE', required=True)

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
database = client[DB_NAME]
tweet_collection = database.get_collection("tweet")
user_collection = database.get_collection("user")


async def fetch_tweets(user_id: str, last_tweet_id_str: str = "", limit: int = 100) -> List[entity.Tweet]:
    user_record = await _fetch_user_record(user_id)
    if user_record is None:
        return []
    user: dict = get_dict_value(user_record, 'user')
    user_id_str = get_dict_value(user, 'id_str')

    search_dict = {"user.id_str": user_id_str}
    if len(last_tweet_id_str) != 0:
        search_dict = {
            '$and': [
                search_dict,
                {"id_str": {'$lt': last_tweet_id_str}}
            ]}

    tweets = tweet_collection.find(search_dict)
    return [entity.Tweet(tweet_record) async for tweet_record in tweets.sort('id', pymongo.DESCENDING).limit(limit)]


async def fetch_search_tweets(search_query: str = "") -> List[entity.Tweet]:
    if search_query is None or len(search_query.strip()) == 0:
        return []
    search_word_list = [{'text': {'$regex': x}} for x in search_query.strip().split() if len(x) != 0]
    search_dict = {'$and': search_word_list}

    tweets = tweet_collection.find(search_dict)
    return [entity.Tweet(tweet_record) async for tweet_record in tweets.sort('id', pymongo.DESCENDING)]


async def fetch_tweet(tweet_id: str) -> entity.Tweet:
    tweet = await tweet_collection.find_one({"id_str": tweet_id})
    if tweet is None:
        return None

    return entity.Tweet(tweet)


async def fetch_user_profile(user_id: str) -> Optional[entity.UserProfile]:
    record = await _fetch_user_record(user_id)
    if record is None:
        return None

    user: dict = get_dict_value(record, 'user')
    user_id_str = get_dict_value(user, 'id_str')
    if user_id == user_id_str:
        return entity.UserProfile(record)

    record = await _fetch_user_record(user_id_str)
    return entity.UserProfile(record)


async def _fetch_user_record(user_id: str) -> Optional[dict]:
    search_dict = {'$or': [{"user.id_str": user_id}, {"user.screen_name": user_id}]}
    return await user_collection.find_one(search_dict, sort=[('_id', pymongo.DESCENDING)])
