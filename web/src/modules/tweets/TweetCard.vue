<script lang="ts">
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { ref, computed, defineComponent, toRefs } from 'vue'
import { useStore } from '../../store'
import {Media, Tweet} from './types'
import IconEllipsisH from '../../icons/IconEllipsisH.vue'
import IconComment from '../../icons/IconComment.vue'
import IconRetweet from '../../icons/IconRetweet.vue'
import IconHeart from '../../icons/IconHeart.vue'
import IconShare from '../../icons/IconShare.vue'
import { Action } from '../storeActionTypes'
import { linkifyHTMLText } from '../../utils/linkify'
import { useRouter } from 'vue-router'
import MediaContent from "../../shared/MediaContent.vue";

export default defineComponent({
  name: 'TweetCard',
  components: {
    IconComment,
    IconEllipsisH,
    IconRetweet,
    IconHeart,
    IconShare,
    MediaContent,
  },
  props: {
    tweet: {
      type: Object as () => Tweet,
      required: true,
    },
  },
  setup(props) {
    const store = useStore()
    const router = useRouter()
    const { tweet } = toRefs(props)
    const favoritesCount = ref(tweet.value.favoritesCount)
    const alreadyLiked = ref(tweet.value.alreadyLiked)
    const retweetsCount = ref(tweet.value.retweetsCount)
    const alreadyRetweeted = ref(tweet.value.alreadyRetweeted)

    const parsedCreatedAt = computed(() => {
      dayjs.extend(relativeTime)
      return dayjs(tweet.value.createdAt).fromNow()
    })

    const parsedContent = computed(() => linkifyHTMLText(tweet.value.content))

    function showOverlay(media: Media) {
      if (media.mediaType == 'video') {
        return
      }
      store.dispatch(Action.TweetsActionTypes.TOGGLE_TWEET_MEDIA_OVERLAY, {
        tweet: tweet.value,
        show: true,
        source: media,
      })
    }

    return {
      router,
      alreadyLiked,
      alreadyRetweeted,
      favoritesCount,
      retweetsCount,
      parsedCreatedAt,
      parsedContent,
      showOverlay,
    }
  },
})
</script>

<template>
  <div
    class="
      w-full
      p-4
      border-b border-lighter
      dark:border-dark
      hover:bg-lighter
      dark:hover:bg-darker dark:hover:bg-opacity-30
      transition-colors
      duration-75
    "
  >
    <div
      v-if="tweet.isRetweet"
      class="ml-6 mb-4 flex space-x-6 text-gray"
    >
      <IconRetweet />
      <span class="font-bold">{{ tweet.retweetAuthorHandle }} Retweeted</span>
    </div>
    <div class="flex">
      <router-link :to="`/${tweet.authorHandle}`" class="flex-none mr-4">
        <img
          v-lazy="tweet.authorPhotoURL"
          class="h-12 w-12 rounded-full flex-none"
        />
      </router-link>
      <div class="w-full">
        <div class="flex flex-wrap items-center w-full">
          <router-link
            :to="`/${tweet.authorHandle}`"
            class="flex flex-wrap items-center"
          >
            <p class="font-semibold dark:text-lightest hover:underline">
              {{ tweet.authorName }}
            </p>
            <p class="text-sm text-dark dark:text-light ml-2">
              @{{ tweet.authorHandle }} ·
            </p>
          </router-link>
          <router-link
            :to="`/${tweet.authorHandle}/status/${tweet.id_str}`"
            class="flex-none mr-4"
          >
            <p class="text-sm text-dark dark:text-light ml-2 hover:underline">
              {{ parsedCreatedAt }}
            </p>
          </router-link>
        </div>
        <div
          class="py-2 break-words dark:text-lightest"
          v-html="parsedContent"
        ></div>
        <div
          v-if="tweet.mediaContents !== null && tweet.mediaContents.length > 0"
          class="relative overflow-hidden w-full h-96 rounded-lg"
        >
          <div class="box-border relative">
            <div
              v-if="tweet.mediaContents.length > 1"
              class="grid grid-cols-2 gap-1 h-full"
            >
              <div
                class="w-full"
                :class="tweet.mediaContents.length > 2 ? 'h-48' : 'h-96'"
              >
                <MediaContent
                    :media="tweet.mediaContents[0]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.mediaContents[0])">
                </MediaContent>
                <MediaContent
                    v-if="tweet.mediaContents.length > 2"
                    :media="tweet.mediaContents[1]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.mediaContents[1])">
                </MediaContent>
              </div>
              <div
                class="w-full"
                :class="tweet.mediaContents.length > 2 ? 'h-48' : 'h-96'"
              >
                <MediaContent
                    v-if="tweet.mediaContents.length > 2"
                    :media="tweet.mediaContents[2]"
                    :clazz="tweet.mediaContents.length === 4 ? 'h-full' : 'h-96' + 'object-cover w-full'"
                    @click.stop="showOverlay(tweet.mediaContents[2])">
                </MediaContent>
                <MediaContent
                    v-else
                    :media="tweet.mediaContents[1]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.mediaContents[1])">
                </MediaContent>
                <MediaContent
                    v-if="tweet.mediaContents.length === 4"
                    :media="tweet.mediaContents[3]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.mediaContents[3])">
                </MediaContent>
              </div>
            </div>
            <div v-else class="w-full">
              <MediaContent
                  :media="tweet.mediaContents[0]"
                  clazz="object-cover w-full h-96"
                  @click.stop="showOverlay(tweet.mediaContents[0])">
              </MediaContent>
            </div>
          </div>
        </div>
        <div class="flex items-center justify-between w-full mt-2">
          <div
            class="
              flex
              items-center
              group
              text-dark
              dark:text-light
              hover:text-blue
              dark:hover:text-blue
            "
          >
            <div
              class="
                mr-3
                p-2
                group-hover:bg-darkblue group-hover:bg-opacity-20
                rounded-full
              "
            >
              <IconComment />
            </div>
            <p class="text-sm">
              {{ tweet.repliesCount }}
            </p>
          </div>
          <div
            class="flex items-center group"
            :class="
              alreadyRetweeted
                ? ['text-success']
                : [
                    'text-dark',
                    'dark:text-light',
                    'hover:text-success',
                    'dark:hover:text-success',
                  ]
            "
          >
            <div
              class="
                mr-3
                p-2
                group-hover:bg-success group-hover:bg-opacity-20
                rounded-full
              "
            >
              <IconRetweet />
            </div>
            <p class="text-sm">
              {{ retweetsCount }}
            </p>
          </div>
          <div
            class="flex items-center group"
            :class="
              alreadyLiked
                ? ['text-danger']
                : [
                    'text-dark',
                    'dark:text-light',
                    'hover:text-danger',
                    'dark:hover:text-danger',
                  ]
            "
          >
            <div
              class="
                mr-3
                p-2
                group-hover:bg-danger group-hover:bg-opacity-20
                rounded-full
              "
            >
              <IconHeart :class="alreadyLiked ? 'fill-current' : null" />
            </div>
            <p class="text-sm">
              {{ favoritesCount }}
            </p>
          </div>
          <div
            class="
              flex
              items-center
              text-dark
              dark:text-light
              hover:text-darkblue
              dark:hover:text-darkblue
            "
          >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
