import { GetterTree } from 'vuex'
import { State } from './state'
import {Media, Tweet, TweetAndReplies} from '../types'

export type Getters = {
  tweetsFeed(state: State): Tweet[]
  lastTweetFeedItem(state: State): Tweet
  tweetStatus(state: State): TweetAndReplies
  lastStatusReplyItem(state: State): Tweet
  tweetsSearchResults(state: State): Tweet[]
  tweetMediaOverlay(state: State): {
    tweet?: Tweet
    show: boolean
    source: Media
  }
}

export const getters: GetterTree<State, State> & Getters = {
  tweetsFeed(state): Tweet[] {
    return state.tweetsFeed
  },
  lastTweetFeedItem(state): Tweet {
    return state.tweetsFeed[state.tweetsFeed.length - 1]
  },
  tweetStatus(state): TweetAndReplies {
    return state.tweetStatus
  },
  lastStatusReplyItem(state: State): Tweet {
    return state.tweetStatus.replies[state.tweetStatus.replies.length - 1]
  },
  tweetsSearchResults(state: State): Tweet[] {
    return state.tweetSearchResult
  },
  tweetMediaOverlay(state: State) {
    return state.tweetMediaOverlay
  },
}
