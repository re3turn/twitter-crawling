import {Media, Tweet, TweetAndReplies} from '../types'

export type State = {
  tweetsFeed: Tweet[]
  tweetStatus: TweetAndReplies
  tweetSearchResult: Tweet[]
  tweetMediaOverlay: {
    tweet?: Tweet
    replies?: Tweet[]
    show: boolean
    source: Media
  }
}

export const state: State = {
  tweetsFeed: [],
  tweetStatus: {
    id: 0,
    content: '',
    mediaContents: [],
    authorName: '',
    authorHandle: '',
    authorPhotoURL: '',
    favoritesCount: 0,
    repliesCount: 0,
    createdAt: '',
    alreadyLiked: false,
    isReply: false,
    replies: [],
  },
  tweetSearchResult: [],
  tweetMediaOverlay: {
    show: false,
    source: {mediaType: '', url: ''} as Media,
  },
}
