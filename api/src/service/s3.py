import re

from src.utils.env import Env


class S3:
    _endpoint_url: str = Env.get_environment('S3_ENDPOINT_URL', required=True)
    _bucket_name: str = Env.get_environment('BUCKET_NAME', required=True)

    @staticmethod
    def gen_s3_key(url) -> str:
        url = re.sub(r'^http[s]*://', '', url)
        return re.sub(r'\?.*$', '', url)

    @classmethod
    def gen_s3_url(cls, url) -> str:
        return f'{cls._endpoint_url}/{cls._bucket_name}/{S3.gen_s3_key(url)}'
