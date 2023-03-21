#!/usr/bin/python3
import dataclasses
import logging
from typing import Any, Dict, List

import pendulum
import tweepy  # type: ignore
from pymongo import MongoClient  # type: ignore

from app.env import Env
from app.save_media import Media


@dataclasses.dataclass
class TwitterUser(object):
    id: str = ''
    since_id: int = 1


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret) -> None:
        self.tweet_page: int = int(Env.get_environment('TWEET_PAGES', default='25'))
        self.tweet_count: int = int(Env.get_environment('TWEET_COUNT', default='200'))
        self._db_url: str = Env.get_environment('DATABASE_URL', required=True)
        self._db_name: str = Env.get_environment('MONGO_DATABASE', required=True)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api: tweepy.API = tweepy.API(auth, retry_count=3, retry_delay=5,
                                           retry_errors={500, 503}, wait_on_rate_limit=True)

        self._media = Media()

        logger.debug(f'Setting info. _db_url={self._db_url}')

    def save_tweets(self, user: TwitterUser) -> None:
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            with MongoClient(self._db_url) as client:
                # If it doesn't exist, it will be created.
                database = client[self._db_name]

                user.since_id = self._fetch_last_tweet_id(database, user.id)
                logger.info(f'Get tweets. user={user.id}. pages={self.tweet_page}, count={self.tweet_count}, '
                            f'since_id={user.since_id}')
                for tweets in tweepy.Cursor(self._api.user_timeline,
                                            user_id=user.id,
                                            tweet_mode='extended',
                                            count=self.tweet_count,
                                            since_id=user.since_id).pages(self.tweet_page):
                    for tweet in tweets:
                        if user.since_id < tweets.since_id:
                            user.since_id = tweets.since_id

                        self._insert_tweet(database, tweet._json)
                        self._insert_user(database, tweet._json)
                        self._update_since_id(database, user.id, str(user.since_id))
        except Exception as e:
            logger.error(e)

    def _insert_tweet(self, database: Any, status_json: Any) -> None:
        if 'user' in status_json and 'id_str' in status_json:
            return

        user = status_json['user']
        exists = self._fetch_tweet(database, user["id_str"])
        if not exists:
            database.tweet.insert_one(status_json)

            logger.info(f'Tweet collected. user = {user["screen_name"]}, user_id = {user["id_str"]}, '
                        f'tweet_id = {status_json["id_str"]}')
            media_urls: List[Dict] = self._media.save_tweet_media(status_json, user["id_str"])
            self._insert_media(database, media_urls)

    def _insert_user(self, database: Any, status_json: Any) -> None:
        if 'user' not in status_json:
            return
        user_json = status_json['user']
        user_status = self._api.get_user(user_id=user_json['id_str'])
        user_dict = {
            'id_str': user_json['id_str'],
            'screen_name': user_json['screen_name'],
            'user': user_status._json,
            'updated_at': pendulum.now()
        }
        filter_dict = {'id_str': user_json['id_str'], 'screen_name': user_json['screen_name']}
        update_dict = {'$set': user_dict}

        database.user.update_one(filter_dict, update_dict, upsert=True)

    @staticmethod
    def _insert_media(database: Any, media_urls: List[Dict]) -> None:
        if len(media_urls) == 0:
            return
        database.media.insert_many(media_urls)

    @staticmethod
    def _fetch_tweet(database: Any, tweet_id_str: str) -> bool:
        tweet_collection = database.get_collection("tweet")
        tweet = tweet_collection.find_one({"id_str": tweet_id_str})
        if tweet is None:
            return False

        return True

    @staticmethod
    def _fetch_last_tweet_id(database: Any, tweet_id_str: str) -> int:
        last_tweet_id_collection = database.get_collection("last_tweet_id")
        last_tweet_id = last_tweet_id_collection.find_one({"id_str": tweet_id_str})
        if last_tweet_id is None:
            return 1

        return int(last_tweet_id['last_tweet_id'])

    @staticmethod
    def _update_since_id(database: Any, user_id_str: str, tweet_id_str: str) -> None:
        since_id_dict = {
            'id_str': user_id_str,
            'last_tweet_id': tweet_id_str,
        }
        filter_dict = {'id_str': user_id_str}
        update_dict = {'$set': since_id_dict}

        database.last_tweet_id.update_one(filter_dict, update_dict, upsert=True)


logger: logging.Logger = logging.getLogger(__name__)
