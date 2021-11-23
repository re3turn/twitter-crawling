<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useStore } from '../../store'
import {
  emptyTweet
} from '../tweets/service'
import { Action } from '../storeActionTypes'
import TweetMediaOverlay from '../tweets/TweetMediaOverlay.vue'
import TrendingSidebar from './TrendingSidebar.vue'
import {Media} from "../tweets/types";

export default defineComponent({
  components: { TrendingSidebar, TweetMediaOverlay },
  name: 'BaseLayout',
  setup() {
    const store = useStore()

    const tweetMediaOverlay = computed(() => store.getters['tweetMediaOverlay'])

    function closeTweetMediaOverlay() {
      store.dispatch(Action.TweetsActionTypes.TOGGLE_TWEET_MEDIA_OVERLAY, {
        tweet: emptyTweet(),
        show: false,
        source: {mediaType: '', url: ''} as Media,
      })
    }

    return { tweetMediaOverlay, closeTweetMediaOverlay }
  },
})
</script>

<template>
  <metainfo>
    <template v-slot:title="{ content }">{{ content ? `${content} | tweet` : `tweet` }}</template>
  </metainfo>
  <TweetMediaOverlay
    :media="tweetMediaOverlay.source"
    :show="tweetMediaOverlay.show"
    :tweet="tweetMediaOverlay.tweet"
    @close="closeTweetMediaOverlay"
  />
  <div class="flex container mx-auto px-4 xl:px-40 h-screen w-full font-sans">
    <router-view />
    <TrendingSidebar />
  </div>
</template>
