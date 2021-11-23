from typing import List, Any

from src.models.media import Media
from src.utils.twitter import TwitterUtils
from src.utils.util import get_dict_value


class RepliedTweet:
    id: int
    id_str: str
    content: str
    medias: List[Media]
    author_name: str
    author_handle: str
    author_photo_url: str
    favorites_count: int
    replies_count: int
    retweets_count: int
    already_liked: bool

    def __init__(self, record: dict):
        self.id = get_dict_value(record, 'id')
        self.id_str = get_dict_value(record, 'id_str')
        self.content = get_dict_value(record, 'text')
        self.medias = TwitterUtils.get_twitter_medias(get_dict_value(record, 'extended_entities'))
        user: dict = get_dict_value(record, 'user')
        self.author_name = TwitterUtils.get_user_name(user)
        self.author_handle = TwitterUtils.get_user_screen_name(user)
        self.author_photo_url = TwitterUtils.get_user_profile_image_url(user)
        self.favorites_count = get_dict_value(record, 'favorite_count')
        self.replies_count = get_dict_value(record, 'reply_count')
        self.retweets_count = get_dict_value(record, 'retweet_count')
        self.already_liked = get_dict_value(record, 'favorited')


class Tweet:
    id: int
    id_str: str
    content: str
    medias: List[Media]
    author_name: str
    author_handle: str
    author_photo_url: str
    replied_to: RepliedTweet
    favorites_count: int
    replies_count: int
    retweets_count: int
    is_reply: bool
    already_liked: bool
    created_at: str
    is_retweet: bool
    retweet_author_handle: str
    already_retweeted: bool

    def __init__(self, record: dict):
        self.id = get_dict_value(record, 'id')
        self.id_str = get_dict_value(record, 'id_str')
        self.content = get_dict_value(record, 'text')
        self.medias = TwitterUtils.get_twitter_medias(get_dict_value(record, 'extended_entities'))
        user: dict = get_dict_value(record, 'user')
        self.author_name = TwitterUtils.get_user_name(user)
        self.author_handle = TwitterUtils.get_user_screen_name(user)
        self.author_photo_url = TwitterUtils.get_user_profile_image_url(user)
        self.replied_to = None
        self.favorites_count = get_dict_value(record, 'favorite_count')
        self.replies_count = get_dict_value(record, 'reply_count')
        self.retweets_count = get_dict_value(record, 'retweet_count')
        self.is_reply = False
        self.already_liked = get_dict_value(record, 'favorited')
        self.created_at = get_dict_value(record, 'created_at')
        retweeted_status: dict = get_dict_value(record, 'retweeted_status')
        self.is_retweet = TwitterUtils.isRetweeted(retweeted_status)
        self.retweet_author_handle = TwitterUtils.get_retweet_author_screen_name(retweeted_status)
        self.already_retweeted = get_dict_value(record, 'retweeted')


class UserProfile:
    id: int
    id_str: str
    name: str
    handle: str
    bio: str
    location: str
    website: str
    birth_date: str
    photo_url: str
    followers_count: int
    followings_count: int
    is_following: bool
    joined_at: str

    def __init__(self, record: dict):
        user: dict = get_dict_value(record, 'user')
        self.id = get_dict_value(user, 'id')
        self.id_str = get_dict_value(user, 'id_str')
        self.name = get_dict_value(user, 'name')
        self.handle = get_dict_value(user, 'screen_name')
        self.bio = get_dict_value(user, 'description')
        self.location = get_dict_value(user, 'location')
        self.website = TwitterUtils.get_expanded_web_url(user)
        self.birth_date = None
        self.photo_url = get_dict_value(user, 'profile_image_url_https').replace('_normal', '')
        self.followers_count = get_dict_value(user, 'followers_count')
        self.followings_count = get_dict_value(user, 'friends_count')
        self.is_following = False
        self.joined_at = get_dict_value(user, 'created_at')


class ResponseItems:
    items: List[Any]
    total_items: int

    def __init__(self, items: List[Any]):
        self.items = items
        self.total_items = len(items)
