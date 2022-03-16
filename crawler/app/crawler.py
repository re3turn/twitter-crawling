#!/usr/bin/python3

import logging
from typing import List

from app.TwitterStream import TwitterStream
from app.env import Env
from app.log import Log


class Crawler:
    def __init__(self) -> None:
        consumer_key: str = Env.get_environment('TWITTER_CONSUMER_KEY', required=True)
        consumer_secret: str = Env.get_environment('TWITTER_CONSUMER_SECRET', required=True)
        access_token: str = Env.get_environment('TWITTER_ACCESS_TOKEN', required=True)
        access_token_secret: str = Env.get_environment('TWITTER_ACCESS_TOKEN_SECRET', required=True)
        self.streamer: TwitterStream = TwitterStream(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                                     access_token=access_token, access_token_secret=access_token_secret)

    def main(self) -> None:
        user_ids: str = Env.get_environment('TWITTER_USER_IDS', required=True)
        user_id_list: List[str] = user_ids.split(',')
        self.streamer.filter(follow=user_id_list)


logger: logging.Logger = logging.getLogger(__name__)

if __name__ == '__main__':
    Log.init_logger(log_name='crawler')
    logger = logging.getLogger(__name__)
    crawler = Crawler()
    crawler.main()
