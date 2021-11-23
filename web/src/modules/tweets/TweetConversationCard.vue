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

enum TweetTypeCode {
  TWEET,
  REPLY,
}

export default defineComponent({
  name: 'TweetConversationCard',
  components: { IconComment, IconEllipsisH, IconRetweet, IconHeart, IconShare, MediaContent },
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

    const replyFavoritesCount = ref(tweet.value.favoritesCount)
    const replyAlreadyLiked = ref(tweet.value.alreadyLiked)

    const repliedTweetFavoritesCount = ref(tweet.value.repliedTo.favoritesCount)
    const repliedTweetAlreadyLiked = ref(tweet.value.repliedTo.alreadyLiked)

    const parsedCreatedAt = computed(() => {
      dayjs.extend(relativeTime)
      return dayjs(tweet.value.createdAt).fromNow()
    })

    const parsedReplyContent = computed(() =>
      linkifyHTMLText(tweet.value.content)
    )

    const parsedRepliedTweetContent = computed(() =>
      linkifyHTMLText(tweet.value.repliedTo.content)
    )

    const replyAlreadyLikedClasses = computed(() => {
      return replyAlreadyLiked.value
        ? ['text-danger']
        : [
            'text-dark',
            'dark:text-light',
            'hover:text-danger',
            'dark:hover:text-danger',
          ]
    })

    const repliedTweetAlreadyLikedClasses = computed(() => {
      return repliedTweetAlreadyLiked.value
        ? ['text-danger']
        : [
            'text-dark',
            'dark:text-light',
            'hover:text-danger',
            'dark:hover:text-danger',
          ]
    })

    function showOverlay(media: Media) {
      if(media.mediaType == 'video') {
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
      replyAlreadyLiked,
      replyFavoritesCount,
      repliedTweetFavoritesCount,
      repliedTweetAlreadyLiked,
      parsedCreatedAt,
      parsedReplyContent,
      parsedRepliedTweetContent,
      replyAlreadyLikedClasses,
      repliedTweetAlreadyLikedClasses,
      TweetTypeCode,
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
      hover:bg-lighter
      dark:hover:bg-darker dark:hover:bg-opacity-30
      cursor-pointer
      transition-colors
      duration-75
    "
    @click="
      router.push(
        `/${tweet.repliedTo.authorHandle}/status/${tweet.repliedTo.id}`
      )
    "
  >
    <div class="flex">
      <div class="flex-none mr-4">
        <router-link :to="`/${tweet.repliedTo.authorHandle}`">
          <img
            v-lazy="tweet.repliedTo.authorPhotoURL"
            class="h-12 w-12 rounded-full flex-none"
          />
        </router-link>
        <div class="h-full w-1 ml-6 bg-dark"></div>
      </div>
      <div class="w-full">
        <div class="flex flex-wrap items-center w-full">
          <router-link
            :to="`/${tweet.repliedTo.authorHandle}`"
            class="flex flex-wrap items-center"
          >
            <p class="font-semibold dark:text-lightest hover:underline">
              {{ tweet.repliedTo.authorName }}
            </p>
            <p class="text-sm text-dark dark:text-light ml-2">
              @{{ tweet.repliedTo.authorHandle }} ·
            </p>
            <p class="text-sm text-dark dark:text-light ml-2">
              {{ parsedCreatedAt }}
            </p>
          </router-link>
          <div
            class="
              text-gray
              ml-auto
              p-2
              hover:bg-darkblue
              hover:text-blue
              hover:bg-opacity-20
              rounded-full
            "
          >
            <IconEllipsisH />
          </div>
        </div>
        <div
          class="py-2 break-words dark:text-lightest"
          v-html="parsedRepliedTweetContent"
        ></div>
        <div
          v-if="
            tweet.repliedTo.mediaContents !== null &&
            tweet.repliedTo.mediaContents.length > 0
          "
          class="relative overflow-hidden w-full h-96 rounded-lg"
        >
          <div class="box-border relative">
            <div
              v-if="tweet.repliedTo.mediaContents.length > 1"
              class="grid grid-cols-2 gap-1 h-full"
            >
              <div
                class="w-full"
                :class="tweet.repliedTo.mediaContents.length > 2 ? 'h-48' : 'h-96'"
              >
                <MediaContent
                    :media="tweet.repliedTo.mediaContents[0]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.repliedTo.mediaContents[0])">
                </MediaContent>
                <MediaContent
                    v-if="tweet.repliedTo.mediaContents.length > 2"
                    :media="tweet.repliedTo.mediaContents[1]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.repliedTo.mediaContents[1])">
                </MediaContent>
              </div>
              <div
                class="w-full"
                :class="tweet.repliedTo.mediaContents.length > 2 ? 'h-48' : 'h-96'"
              >
                <MediaContent
                    v-if="tweet.repliedTo.mediaContents.length > 2"
                    :media="tweet.repliedTo.mediaContents[2]"
                    :clazz="tweet.repliedTo.mediaContents.length === 4 ? 'h-full' : 'h-96' + 'object-cover w-full'"
                    @click.stop="showOverlay(tweet.repliedTo.mediaContents[2])">
                </MediaContent>
                <MediaContent
                    v-else
                    :media="tweet.repliedTo.mediaContents[1]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.repliedTo.mediaContents[1])">
                </MediaContent>
                <MediaContent
                    v-if="tweet.repliedTo.mediaContents.length === 4"
                    :media="tweet.repliedTo.mediaContents[3]"
                    clazz="object-cover w-full h-full"
                    @click.stop="showOverlay(tweet.repliedTo.mediaContents[3])">
                </MediaContent>
              </div>
            </div>
            <div v-else class="w-full">
              <MediaContent
                  :media="tweet.repliedTo.mediaContents[0]"
                  clazz="object-cover w-full h-96"
                  @click.stop="showOverlay(tweet.repliedTo.mediaContents[0])">
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
              {{ tweet.repliedTo.repliesCount }}
            </p>
          </div>
          <div
            class="
              flex
              items-center
              group
              text-dark
              dark:text-light
              hover:text-success
              dark:hover:text-success
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
              {{ tweet.repliedTo.repliesCount }}
            </p>
          </div>
          <div
            class="flex items-center group"
            :class="repliedTweetAlreadyLikedClasses"
          >
            <div
              class="
                mr-3
                p-2
                group-hover:bg-danger group-hover:bg-opacity-20
                rounded-full
              "
            >
              <IconHeart
                :class="repliedTweetAlreadyLiked ? 'fill-current' : null"
              />
            </div>
            <p class="text-sm">
              {{ repliedTweetFavoritesCount }}
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
            <div
              class="
                mr-3
                p-2
                hover:bg-darkblue hover:bg-opacity-20
                rounded-full
              "
            >
              <IconShare />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    class="
      w-full
      p-4
      border-b border-lighter
      dark:border-dark
      hover:bg-lighter
      dark:hover:bg-darker dark:hover:bg-opacity-30
      cursor-pointer
      transition-colors
      duration-75
    "
    @click="router.push(`/${tweet.authorHandle}/status/${tweet.id_str}`)"
  >
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
            <p class="text-sm text-dark dark:text-light ml-2">
              {{ parsedCreatedAt }}
            </p>
          </router-link>
          <div
            class="
              text-gray
              ml-auto
              p-2
              hover:bg-darkblue
              hover:text-blue
              dark:hover:text-blue
              hover:bg-opacity-20
              rounded-full
            "
          >
            <IconEllipsisH />
          </div>
        </div>
        <div class="pb-2 break-words">
          <span class="text-gray">Replying to</span>
          <router-link :to="`/${tweet.repliedTo.authorHandle}`">
            <span class="text-blue hover:underline">
              @{{ tweet.repliedTo.authorHandle }}
            </span>
          </router-link>
        </div>
        <div
          class="py-2 break-words dark:text-lightest"
          v-html="parsedReplyContent"
        ></div>
        <div
          v-if="tweet.mediaContents !== null && tweet.mediaContents.length > 0"
          class="relative overflow-hidden w-full h-96 rounded-lg"
        >
          <div class="box-border relative">
            <div class="grid grid-cols-2 gap-1 h-full">
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
            class="
              flex
              items-center
              group
              text-dark
              dark:text-light
              hover:text-success
              dark:hover:text-success
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
              {{ tweet.repliesCount }}
            </p>
          </div>
          <div
            class="flex items-center group"
            :class="replyAlreadyLikedClasses"
          >
            <div
              class="
                mr-3
                p-2
                group-hover:bg-danger group-hover:bg-opacity-20
                rounded-full
              "
            >
              <IconHeart :class="replyAlreadyLiked ? 'fill-current' : null" />
            </div>
            <p class="text-sm">
              {{ replyFavoritesCount }}
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
            <div
              class="
                mr-3
                p-2
                hover:bg-darkblue hover:bg-opacity-20
                rounded-full
              "
            >
              <IconShare />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
