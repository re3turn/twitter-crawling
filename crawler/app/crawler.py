#!/usr/bin/python3

import logging
from typing import List

import time

from app.Twitter import Twitter, TwitterUser
from app.env import Env
from app.log import Log


class Crawler:
    def __init__(self) -> None:
        consumer_key: str = Env.get_environment('TWITTER_CONSUMER_KEY', required=True)
        consumer_secret: str = Env.get_environment('TWITTER_CONSUMER_SECRET', required=True)
        access_token: str = Env.get_environment('TWITTER_ACCESS_TOKEN', required=True)
        access_token_secret: str = Env.get_environment('TWITTER_ACCESS_TOKEN_SECRET', required=True)
        self.twitter: Twitter = Twitter(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                        access_token=access_token, access_token_secret=access_token_secret)

    def main(self) -> None:
        interval_minutes: int = int(Env.get_environment('INTERVAL', default='5'))
        user_ids: str = Env.get_environment('TWITTER_USER_IDS', required=True)

        user_list: List[TwitterUser] = [TwitterUser(id=user_id) for user_id in user_ids.split(',')]

        while True:
            try:
                for user in user_list:
                    logger.info(f'Crawling start. user = {user.id}')
                    self.twitter.save_tweets(user)
            except Exception as e:
                logger.exception(f'Crawling error exception={e.args}')

            logger.info(f'Interval. sleep {interval_minutes} minutes.')
            time.sleep(interval_minutes * 60)


logger: logging.Logger = logging.getLogger(__name__)

if __name__ == '__main__':
    Log.init_logger(log_name='crawler')
    logger = logging.getLogger(__name__)
    crawler = Crawler()
    crawler.main()
