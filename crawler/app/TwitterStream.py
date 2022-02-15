#!/usr/bin/python3
import json
import logging
from typing import Any, Dict, List

import pendulum
import tweepy  # type: ignore
from pymongo import MongoClient

from app.env import Env
from app.save_media import Media


class TwitterStream(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret) -> None:
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self._db_url: str = Env.get_environment('DATABASE_URL', required=True)
        self._db_name: str = Env.get_environment('MONGO_DATABASE', required=True)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api: tweepy.API = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

        self._media = Media()

        logger.debug(f'Setting info. _db_url={self._db_url}')

    # This is a class provided by tweepy to access the Twitter Streaming API.
    def on_connect(self):
        # Called initially to connect to the Streaming API
        logger.info("You are now connected to the streaming API.")

    def on_request_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        logger.error('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, tweepy_status):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            with MongoClient(self._db_url) as client:
                # If it doesn't exist, it will be created.
                database = client[self._db_name]
                status_json = json.loads(tweepy_status)

                self._insert_tweet(database, status_json)
                self._insert_user(database, status_json)
        except Exception as e:
            logger.error(e)

    def _insert_tweet(self, database: Any, status_json: Any) -> None:
        if 'delete' in status_json:
            TwitterStream._delete_status(database, status_json)
        else:
            database.tweet.insert_one(status_json)
            if 'user' in status_json and 'id_str' in status_json:
                user = status_json['user']
                logger.info(f'Tweet collected. user = {user["screen_name"]}, user_id = {user["id_str"]}, '
                            f'tweet_id = {status_json["id_str"]}')
                media_urls: List[Dict] = self._media.save_tweet_media(status_json, user["id_str"])
                self._insert_media(database, media_urls)

    def _insert_user(self, database: Any, status_json: Any) -> None:
        if 'delete' in status_json:
            return
        if 'user' not in status_json:
            return
        user_json = status_json['user']
        user_status = self._api.get_user(user_id=user_json['id_str'])
        user_dict = {
            'id_str': user_json['id_str'],
            'screen_name': user_json['screen_name'],
            'user': user_status,
            'updated_at': pendulum.now()
        }
        filter_dict = {'id_str': user_json['id_str'], 'screen_name': user_json['screen_name']}
        update_dict = {'$set': user_dict}

        database.user.update_one(filter_dict, update_dict, upsert=True)

    @staticmethod
    def _delete_status(database: Any, status_json: Any) -> None:
        database.delete_tweet.insert_one(status_json)
        delete_status_json = status_json["delete"]
        if 'status' not in delete_status_json:
            return
        if 'id_str' not in delete_status_json['status']:
            return
        if 'user_id_str' not in delete_status_json['status']:
            return

        logger.info(f'Delete tweet. user_id = {delete_status_json["status"]["user_id_str"]}, '
                    f'tweet_id = {delete_status_json["status"]["id_str"]}')

    @staticmethod
    def _insert_media(database: Any, media_urls: List[Dict]) -> None:
        if len(media_urls) == 0:
            return
        database.media.insert_many(media_urls)


logger: logging.Logger = logging.getLogger(__name__)
