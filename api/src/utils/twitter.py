from typing import List

from src.models.media import Media


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
    def get_twitter_medias(extended_entities: dict) -> List[Media]:
        if extended_entities is None or 'media' not in extended_entities:
            return []

        media_list: List[Media] = []
        url = ""
        for media in extended_entities['media']:
            if media['type'] == 'photo':
                url = TwitterUtils._get_photo_url(media)
            elif media['type'] == 'video':
                url = TwitterUtils._get_video_url(media)

            if url:
                media_list.append(Media(media['type'], url))

        return media_list

    @staticmethod
    def get_user_screen_name(user: dict) -> str:
        if user is None or 'screen_name' not in user:
            return ''

        return user['screen_name']

    @staticmethod
    def get_user_name(user: dict) -> str:
        if user is None or 'name' not in user:
            return ''

        return user['name']

    @staticmethod
    def isRetweeted(retweeted_status: dict) -> bool:
        return retweeted_status is not None and len(retweeted_status) > 0

    @staticmethod
    def get_retweet_author_screen_name(retweeted_status: dict) -> str:
        if not TwitterUtils.isRetweeted(retweeted_status):
            return ''

        if 'user' not in retweeted_status:
            return ''

        return TwitterUtils.get_user_screen_name(retweeted_status['user'])

    @staticmethod
    def get_user_profile_image_url(user: dict) -> str:
        if user is None or 'profile_image_url_https' not in user:
            return ''

        return user['profile_image_url_https']

    @staticmethod
    def get_expanded_web_url(user: dict) -> str:
        if user is None or 'entities' not in user:
            return ''
        entities = user['entities']
        if entities is None or 'url' not in entities:
            return ''
        url = entities['url']
        if url is None or 'urls' not in url:
            return ''
        urls = url['urls']

        if len(urls) == 0:
            return ''
        if urls[0] is None or 'expanded_url' not in urls[0]:
            return ''

        return urls[0]['expanded_url']

