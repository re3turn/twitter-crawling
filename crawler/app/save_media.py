import logging
import os
import urllib.error
import shutil
from typing import List, Dict

from app.downloader import Downloader
from app.s3_uploader import S3Uploader
from app.twitter_utils import TwitterUtils


class Media:
    def __init__(self):
        self._downloader = Downloader()
        self._s3 = S3Uploader()

    def save_tweet_media(self, tweet: dict, user_id: str) -> List[Dict]:
        if 'extended_entities' not in tweet:
            return []
        medias: List[Dict] = []
        media_urls: List[str] = TwitterUtils.get_twitter_medias(tweet['extended_entities'])
        for url in media_urls:
            original_image_url = url
            if url.startswith('https://pbs.twimg.com/media') or url.startswith('http://pbs.twimg.com/media'):
                original_image_url = TwitterUtils.make_original_image_url(url)

            if self.save_media(original_image_url, user_id):
                media = {
                    'url': url,
                    's3_key': S3Uploader.gen_s3_key(url)
                }
                medias.append(media)

        return medias

    def save_media(self, url: str, user_id: str) -> bool:
        # download
        download_path: str = self._downloader.make_download_path(url, user_id)
        # if url.startswith('https://pbs.twimg.com/media') or url.startswith('http://pbs.twimg.com/media'):
        #     url = self.twitter.make_original_image_url(url)
        try:
            self._downloader.download_media(url, download_path)
        except urllib.error.HTTPError:
            logger.exception(f'Download failed. media_url={url}')
            return False

        # upload
        is_uploaded: bool = self._s3.upload(download_path, url)

        # delete
        shutil.rmtree(os.path.dirname(download_path))
        logger.debug(f'Delete directory. path={os.path.dirname(download_path)}')

        if not is_uploaded:
            logger.error(f'Upload failed. media_url={url}')
            return False

        return True


logger: logging.Logger = logging.getLogger(__name__)
