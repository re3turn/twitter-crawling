import logging
import os
import re
import urllib
import urllib.error
from retry import retry


class Downloader:
    def __init__(self) -> None:
        self._download_dir: str = './download'

        os.makedirs(self._download_dir, exist_ok=True)

    @staticmethod
    @retry(urllib.error.HTTPError, tries=3, delay=2, backoff=2)
    def download_media(media_url: str, download_path: str) -> None:
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        logger.debug(f'Download file. url={media_url}, path={download_path}')
        urllib.request.urlretrieve(media_url, download_path)  # type: ignore

    def make_download_path(self, url: str, user_id: str) -> str:
        url = re.sub(r'\?.*$', '', url)
        return f'{self._download_dir}/{user_id}/{os.path.basename(url)}'


logger: logging.Logger = logging.getLogger(__name__)
