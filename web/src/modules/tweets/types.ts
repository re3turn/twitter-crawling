export type TweetJSONSchema = {
  id: number
  id_str: string
  content: string
  medias: MediaJSONSchema[] | null
  author_name: string
  author_handle: string
  author_photo_url: string
  replied_to?: Omit<
    TweetJSONSchema,
    | 'replied_to'
    | 'is_reply'
    | 'created_at'
    | 'is_retweet'
    | 'retweet_author_handle'
    | 'already_retweeted'
  >
  is_reply: boolean
  favorites_count: number
  replies_count: number
  retweets_count: number
  created_at: string
  already_liked: boolean
  is_retweet: boolean
  retweet_author_handle: string
  already_retweeted: boolean
}

export type Tweet = {
  id: number
  id_str: string
  content: string
  mediaContents: Media[] | null
  authorName: string
  authorHandle: string
  authorPhotoURL: string
  repliedTo?: Omit<
    Tweet,
    | 'repliedTo'
    | 'isReply'
    | 'createdAt'
    | 'isRetweet'
    | 'retweetAuthorHandle'
    | 'alreadyRetweeted'
  >
  favoritesCount: number
  repliesCount: number
  retweetsCount: number
  isReply: boolean
  alreadyLiked: boolean
  createdAt: string
  isRetweet: boolean
  retweetAuthorHandle: string
  alreadyRetweeted: boolean
}

export type MediaJSONSchema = {
  media_type: string
  url: string
}

export type Media = {
  mediaType: string
  url: string
}

export type TweetAndReplies = Tweet & {
  replies: Tweet[]
}
