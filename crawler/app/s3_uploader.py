import logging
import re

import boto3

from app.env import Env


class S3Uploader:
    def __init__(self):
        _access_key: str = Env.get_environment('AWS_ACCESS_KEY', required=True)
        _secret_key: str = Env.get_environment('AWS_SECRET_KEY', required=True)
        _endpoint_url: str = Env.get_environment('S3_ENDPOINT_URL', required=True)
        self._bucket_name: str = Env.get_environment('BUCKET_NAME', required=True)

        self._client = boto3.client(
            's3',
            aws_access_key_id=_access_key,
            aws_secret_access_key=_secret_key,
            endpoint_url=_endpoint_url,
        )

    @staticmethod
    def gen_s3_key(url) -> str:
        url = re.sub(r'^http[s]*://', '', url)
        return re.sub(r'\?.*$', '', url)

    def upload(self, file_path: str, url) -> bool:
        try:
            self._client.upload_file(file_path, self._bucket_name, self.gen_s3_key(url))
        except Exception as e:
            logger.error(f'Upload failed. media_url={url}, exception={e.args}')
            return False

        return True


logger: logging.Logger = logging.getLogger(__name__)
