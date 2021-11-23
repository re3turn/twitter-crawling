import {Media, Tweet, TweetJSONSchema} from './types'
import axios from '../../utils/axios'
import { ResponseItems } from '../../types'

function parseResponseTweetItem(data: TweetJSONSchema): Tweet {
  const repliedTo = data.replied_to
    ? {
        id: data.replied_to.id,
        id_str: data.replied_to.id_str,
        content: data.replied_to.content,
        mediaContents: data.replied_to.medias?.map( function(media) {
          return { mediaType: media.media_type, url: media.url} as Media;
        }),
        authorName: data.replied_to.author_name,
        authorHandle: data.replied_to.author_handle,
        authorPhotoURL: data.replied_to.author_photo_url,
        favoritesCount: data.replied_to.favorites_count,
        repliesCount: data.replied_to.replies_count,
        alreadyLiked: data.replied_to.already_liked,
        retweetsCount: data.replied_to.retweets_count,
      }
    : undefined
  return {
    mediaContents: data.medias?.map( function(media) {
      return { mediaType: media.media_type, url: media.url} as Media;
    }),
    authorHandle: data.author_handle,
    authorName: data.author_name,
    authorPhotoURL: data.author_photo_url,
    repliedTo,
    favoritesCount: data.favorites_count,
    repliesCount: data.replies_count,
    retweetsCount: data.retweets_count,
    createdAt: data.created_at,
    alreadyLiked: data.already_liked,
    isReply: data.is_reply,
    isRetweet: data.is_retweet,
    retweetAuthorHandle: data.retweet_author_handle,
    alreadyRetweeted: data.already_retweeted,
    ...data,
  } as Tweet
}

export function emptyTweet(): Tweet {
  return {
    id: 0,
    id_str: "0",
    content: "",
    mediaContents: null,
    authorName: "",
    authorHandle: "",
    authorPhotoURL: "",
    repliedTo: null,
    favoritesCount: 0,
    repliesCount: 0,
    retweetsCount: 0,
    isReply: false,
    alreadyLiked: false,
    createdAt: "",
    isRetweet: false,
    retweetAuthorHandle: "",
    alreadyRetweeted: false,
  } as Tweet
}

export async function fetchTweet(tweetId: string): Promise<Tweet> {
  try {
    const { data } = await axios.get<TweetJSONSchema>(`/tweets/${tweetId}`)

    return parseResponseTweetItem(data)
  } catch (error) {
    throw error
  }
}

export async function fetchUserTweets(
  userId: string,
  cursor?: string
): Promise<Tweet[]> {
  try {
    const withCursor = cursor === '' || cursor === undefined
    const target = withCursor
      ? `/users/${userId}/tweets`
      : `/users/${userId}/tweets?cursor=${cursor}`

    const { data } = await axios.get<ResponseItems<TweetJSONSchema>>(target)

    const items = data.items.map((item) => parseResponseTweetItem(item))

    return items
  } catch (error) {
    throw error
  }
}

export async function fetchFeed(cursor?: string): Promise<Tweet[]> {
  try {
    const withCursor = cursor === '' || cursor === undefined
    const target = withCursor ? '/tweets/feed' : `/tweets/feed?cursor=${cursor}`

    const { data } = await axios.get<ResponseItems<TweetJSONSchema>>(target)

    if (data.items === null) {
      return []
    }

    const items = data.items.map((item) => parseResponseTweetItem(item))

    return items
  } catch (error) {
    throw error
  }
}

export async function searchTweets(query: string): Promise<Tweet[]> {
  try {
    const { data } = await axios.get<ResponseItems<TweetJSONSchema>>(
      `/tweets/search?query=${query}`
    )

    if (data.items === null) {
      return []
    }

    const items = data.items.map((item) => parseResponseTweetItem(item))

    return items
  } catch (error) {
    throw error
  }
}

export async function createTweet(
  content: string,
  attachments?: File[]
): Promise<void> {
  try {
    const formData = new FormData()

    formData.append('content', content)
    if (attachments && attachments?.length > 0) {
      attachments.forEach((attachment) => formData.append('photos', attachment))
    }

    await axios.post('/tweets', formData)
  } catch (error) {
    throw error
  }
}

export async function createReply(
  tweetId: string,
  content: string
): Promise<void> {
  try {
    await axios.post(`/tweets/${tweetId}/reply`, { content })
  } catch (error) {
    throw error
  }
}
