import re
from typing import List


class TwitterUtils:
    @staticmethod
    def _get_photo_url(media: dict) -> str:
        if 'media_url_https' in media:
            return media['media_url_https']
        elif 'media_url' in media:
            return media['media_url']

        return ''

    @staticmethod
    def _get_video_url(media: dict) -> str:
        bitrate = 0
        index = 0
        for i, video in enumerate(media['video_info']['variants']):
            if 'bitrate' in video and video['bitrate'] > bitrate:
                bitrate = video['bitrate']
                index = i

        if bitrate > 0:
            return media['video_info']['variants'][index]['url']

        return ''

    @staticmethod
    def get_twitter_medias(extended_entities: dict) -> List[str]:
        if extended_entities is None or 'media' not in extended_entities:
            return []

        media_list: List[str] = []
        url = ""
        for media in extended_entities['media']:
            if media['type'] == 'photo':
                url = TwitterUtils._get_photo_url(media)
            elif media['type'] == 'video':
                url = TwitterUtils._get_video_url(media)

            if url:
                media_list.append(url)

        return media_list

    @staticmethod
    def gen_download_url(url: str) -> str:
        if url.startswith('https://pbs.twimg.com/media') or url.startswith('http://pbs.twimg.com/media'):
            return TwitterUtils.make_original_image_url(url)

        return url

    @staticmethod
    def make_original_image_url(url: str) -> str:
        if '?' in url:
            if 'name=' in url:
                original_url: str = re.sub('name=[a-zA-Z0-9]+', 'name=orig', url)
                return original_url
            else:
                return url + '&name=orig'

        return url + '?name=orig'

    @staticmethod
    def get_user_profile_image_url(user: dict) -> str:
        if user is None or 'profile_image_url_https' not in user:
            return ''

        return user['profile_image_url_https']
