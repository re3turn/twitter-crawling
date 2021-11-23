<script lang="ts">
import dayjs from 'dayjs'
import {
  computed,
  defineComponent,
  onBeforeMount,
  onMounted,
  ref,
  watch,
  watchEffect,
} from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from '../../../store'
import { useScroll } from '../../../hooks/useScroll'
import TweetCard from '../../tweets/TweetCard.vue'
import { Action } from '../../storeActionTypes'
import {Media, TweetAndReplies} from '../../tweets/types'
import TweetCreateReplyDialog from '../../tweets/TweetCreateReplyDialog.vue'
import Return from '../../../shared/Return.vue'
import LoadingSpinner from '../../../shared/LoadingSpinner.vue'
import PageDoesNotExists from '../../../shared/PageDoesNotExists.vue'
import IconEllipsisH from '../../../icons/IconEllipsisH.vue'
import IconComment from '../../../icons/IconComment.vue'
import IconRetweet from '../../../icons/IconRetweet.vue'
import IconShare from '../../../icons/IconShare.vue'
import IconHeart from '../../../icons/IconHeart.vue'
import { linkifyHTMLText } from '../../../utils/linkify'
import { useMeta } from 'vue-meta'
import {tweetMetaTag, userMetaTag} from '../../../utils/metatag.ts'
import MediaContent from "../../../shared/MediaContent.vue";

export default defineComponent({
  components: {
    TweetCard,
    LoadingSpinner,
    TweetCreateReplyDialog,
    Return,
    IconEllipsisH,
    IconComment,
    IconRetweet,
    IconHeart,
    IconShare,
    PageDoesNotExists,
    MediaContent,
  },
  name: 'Status',
  setup() {
    const store = useStore()
    const route = useRoute()
    const notFound = ref(false)
    const initialLoadDone = ref(false)
    const loadNextBatch = ref(false)
    const tweet = ref<TweetAndReplies | null>(null)
    const tweetId = ref<string>(route.params.tweetId as string)

    const [scrollRef, isBottom] = useScroll()

    const showCreateReplyDialog = ref(false)

    const parsedCreatedAt = computed(() =>
      dayjs(store.getters['tweetStatus'].createdAt).format(
        'h:mm A · MMM D, YYYY'
      )
    )

    const parsedContent = computed(() => linkifyHTMLText(tweet.value.content))

    let { meta } = useMeta({
      title: 'tweet',
    })

    watchEffect(() => {
      const tweetValue = tweet.value
      tweetMetaTag(tweetValue, meta)
    })

    onBeforeMount(async () => {
      await getTweetStatus(tweetId.value)
      initialLoadDone.value = true
    })

    onMounted(async () => {
      watch(
        () => route.params.tweetId,
        async (tweetId) => {
          if (tweetId) {
            initialLoadDone.value = false
            await getTweetStatus(tweetId as string)
            initialLoadDone.value = true
          }
        }
      )

      watchEffect(async () => {
        if (!loadNextBatch.value && isBottom.value) {
          isBottom.value = false
        }
      })
    })

    async function getTweetStatus(tweetId: string) {
      try {
        await store
          .dispatch(Action.TweetsActionTypes.GET_TWEET_STATUS, tweetId)
          .catch(() => {
            notFound.value = true
          })
        tweet.value = store.getters['tweetStatus']
      } catch (error) {
      notFound.value = true
      }
    }

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
      scrollRef,
      notFound,
      initialLoadDone,
      loadNextBatch,
      tweet,
      showCreateReplyDialog,
      parsedCreatedAt,
      parsedContent,
      showOverlay,
    }
  },
})
</script>

<template>
  <main
    class="
      w-full
      h-full
      overflow-y-scroll
      border-r border-lighter
      dark:border-darker
      md:border-r-0
    "
    ref="scrollRef"
  >
    <div
      class="
        px-5
        py-3
        border-b border-lighter
        dark:border-dark
        flex
        items-center
        justify-start
        space-x-6
      "
    >
      <Return />
      <h1 class="text-2xl font-bold dark:text-lightest">Tweet</h1>
    </div>
    <div v-if="notFound" class="mt-12 px-5 py-3">
      <PageDoesNotExists />
    </div>
    <div v-else class="px-5 py-3 border-b border-lighter dark:border-dark">
      <div v-if="initialLoadDone && tweet" class="w-full">
        <div class="flex items-center w-full">
          <img
            v-lazy="tweet.authorPhotoURL"
            class="mr-5 h-12 w-12 rounded-full"
          />
          <router-link :to="`/${tweet.authorHandle}`">
            <p class="font-semibold dark:text-lightest hover:underline">
              {{ tweet.authorName }}
            </p>
            <p class="text-sm text-dark dark:text-light">
              @{{ tweet.authorHandle }}
            </p>
          </router-link>
          <div
            class="
              cursor-pointer
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
          class="text-2xl py-2 break-words dark:text-lightest"
          v-html="parsedContent"
        ></div>
        <div
          v-if="tweet.mediaContents !== null && tweet.mediaContents.length > 0"
          class="
            relative
            overflow-hidden
            w-full
            h-96
            rounded-lg
            cursor-pointer
            mb-4
          "
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
        <p class="text-dark dark:text-light">{{ parsedCreatedAt }}</p>
        <div
          class="
            flex
            items-center
            justify-start
            space-x-12
            w-full
            border-t border-b
            my-4
            py-4
            border-lighter
            dark:border-dark
          "
        >
          <div class="flex space-x-2 text-sm">
            <p class="text-light dark:text-lightest font-bold">
              {{ tweet.repliesCount }}
            </p>
            <p class="text-dark dark:text-light">Retweets</p>
          </div>
          <div class="flex space-x-2 text-sm">
            <p class="text-light dark:text-lightest font-bold">
              {{ tweet.favoritesCount }}
            </p>
            <p class="text-dark dark:text-light">Likes</p>
          </div>
        </div>
        <div
          class="
            flex
            items-center
            justify-around
            w-full
            text-xl text-dark
            dark:text-light
          "
        >
          <div
            class="
              flex
              justify-center
              hover:bg-darkblue
              hover:text-blue
              hover:bg-opacity-20
              rounded-full
              p-3
              cursor-pointer
              transition
              duration-75
            "
            @click="showCreateReplyDialog = true"
          >
            <IconComment :size="20" />
          </div>
          <div
            class="
              flex
              justify-center
              hover:bg-success
              hover:text-success
              hover:bg-opacity-20
              rounded-full
              p-3
              cursor-pointer
            "
          >
            <IconRetweet :size="20" />
          </div>
          <div
            class="
              flex
              justify-center
              hover:bg-danger
              hover:text-danger
              hover:bg-opacity-20
              rounded-full
              p-3
              cursor-pointer
            "
            :class="
              tweet.alreadyLiked
                ? ['text-danger']
                : ['text-dark', 'dark:text-light', 'hover:text-danger']
            "
          >
            <IconHeart
              :size="20"
              :class="tweet.alreadyLiked ? 'fill-current' : null"
            />
          </div>
          <div
            class="
              flex
              justify-center
              hover:bg-darkblue
              hover:text-darkblue
              hover:bg-opacity-20
              rounded-full
              p-3
              cursor-pointer
            "
          >
            <IconShare :size="20" />
          </div>
        </div>
      </div>
    </div>
    <div v-show="!initialLoadDone" class="flex flex-col">
      <div class="w-full text-center">
        <LoadingSpinner />
      </div>
    </div>
    <div
      v-if="
        initialLoadDone &&
        !notFound &&
        tweet &&
        tweet.replies &&
        tweet.replies.length > 0
      "
    >
      <TweetCard
        :tweet="reply"
        v-for="reply in tweet.replies"
        :key="reply.id"
      />
      <div
        v-show="
          tweet && tweet.replies && tweet.replies.length > 0 && loadNextBatch
        "
        class="
          w-full
          p-4
          border-b border-lighter
          dark:border-dark
          hover:bg-lighter
          dark:hover:bg-light dark:hover:bg-opacity-20
          flex
          cursor-pointer
          transition-colors
          duration-75
        "
      >
        <div class="w-full text-center">
          <LoadingSpinner />
        </div>
      </div>
    </div>
  </main>
</template>
