<script lang="ts">
import {
  defineComponent,
  onBeforeMount,
  onMounted,
  ref,
  computed,
  watch,
  watchEffect,
} from 'vue'
import { useRoute } from 'vue-router'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { useStore } from '../../store'
import { ProfileDetails } from './types'
import { Action } from '../storeActionTypes'
import { useScroll } from '../../hooks/useScroll'
import TweetCard from '../tweets/TweetCard.vue'
import TweetConversationCard from '../tweets/TweetConversationCard.vue'
import { Tweet } from '../tweets/types'
import Return from '../../shared/Return.vue'
import LoadingSpinner from '../../shared/LoadingSpinner.vue'
import IconEllipsisH from '../../icons/IconEllipsisH.vue'
import IconMapMarker from '../../icons/IconMapMarker.vue'
import IconLink from '../../icons/IconLink.vue'
import IconGift from '../../icons/IconGift.vue'
import IconCalendar from '../../icons/IconCalendar.vue'
import EditProfileDialog from './EditProfileDialog.vue'
import TweetMediaOverlay from '../tweets/TweetMediaOverlay.vue'
import {userMetaTag} from '../../utils/metatag.ts'
import {useMeta} from "vue-meta";

export default defineComponent({
  name: 'Profile',
  components: {
    Return,
    TweetCard,
    TweetConversationCard,
    LoadingSpinner,
    IconEllipsisH,
    IconMapMarker,
    IconLink,
    IconGift,
    IconCalendar,
    EditProfileDialog,
    TweetMediaOverlay,
  },
  setup() {
    const store = useStore()
    const route = useRoute()

    const selectedTab = ref(1)
    const initialLoadDone = ref(false)
    const loadNextBatch = ref(false)
    const showEditProfileDialog = ref(false)
    const tweets = ref<Tweet[]>([])
    const handle = ref(route.params.name as string)

    const [scrollRef, isBottom] = useScroll()

    const tabClasses = ['text-blue', 'border-b-2', 'border-blue']

    const selectedTabClasses = [
      'dark:text-gray',
      'border-b-2',
      'border-dark',
      'border-opacity-0',
    ]

    const profile = computed(() => store.getters['profileInfo'])

    // Check if profile birthdate is set or not because it is set to "" by default.
    const validBirthDate = computed(() => {
      dayjs.extend(relativeTime)
      return dayjs(store.getters['profileInfo'].birthDate).isValid()
    })

    const parsedBirthDate = computed(() => {
      dayjs.extend(relativeTime)
      return dayjs(store.getters['profileInfo'].birthDate).format(
        'MMMM D, YYYY'
      )
    })

    const parsedJoinedAt = computed(() => {
      dayjs.extend(relativeTime)
      return dayjs(store.getters['profileInfo'].joinedAt).format('MMMM YYYY')
    })

    const { meta } = useMeta({
      title: 'tweet',
    })

    watchEffect(() => {
      const user = profile.value
      userMetaTag(user, meta)
    })

    onBeforeMount(async () => {
      await store.dispatch(
        Action.UserActionTypes.GET_PROFILE_DETAILS,
        handle.value
      )
      await loadTweets()
      initialLoadDone.value = true
    })

    onMounted(() => {
      watch(
        () => route.params.name,
        async (name) => {
          if (name) {
            initialLoadDone.value = false
            await store.dispatch(
              Action.UserActionTypes.GET_PROFILE_DETAILS,
              name as string
            )
            await loadTweets()
            initialLoadDone.value = true
          }
        }
      )

      watchEffect(async () => {
        if (!loadNextBatch.value && isBottom.value) {
          loadNextBatch.value = true
          await loadTweets()
          loadNextBatch.value = false
          isBottom.value = false
        }
      })
    })

    async function loadTweets() {
      try {
        if (
          initialLoadDone.value &&
          store.getters['profileTweets'].length > 0
        ) {
          const lastItem = store.getters['lastProfileTweet']
          await store.dispatch(
            Action.UserActionTypes.LOAD_MORE_PROFILE_TWEETS,
            {
              handle: handle.value,
              cursor: lastItem.id_str,
            }
          )
        } else {
          await store.dispatch(
            Action.UserActionTypes.GET_PROFILE_TWEETS,
            handle.value
          )
        }

        tweets.value = store.getters['profileTweets']
      } catch (error) {
        initialLoadDone.value = true
      }
    }

    async function updateProfile(payload: ProfileDetails) {
      await store.dispatch(
        Action.UserActionTypes.UPDATE_PROFILE_DETAILS,
        payload
      )
    }

    return {
      selectedTab,
      tabClasses,
      selectedTabClasses,
      showEditProfileDialog,
      scrollRef,
      initialLoadDone,
      loadNextBatch,
      profile,
      tweets,
      validBirthDate,
      parsedBirthDate,
      parsedJoinedAt,
      updateProfile,
    }
  },

})
</script>

<template>
  <EditProfileDialog
    :profile="profile"
    :show="showEditProfileDialog"
    @close="showEditProfileDialog = false"
    @dispatch="updateProfile"
  />

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
      <h1 class="text-xl font-bold dark:text-lightest">{{ profile.name }}</h1>
    </div>
    <div
      class="
        px-6
        h-48
        border-b border-lighter
        dark:border-dark
        bg-blue
        relative
      "
    >
      <div
        class="
          absolute
          overflow-hidden
          rounded-full
          w-28
          h-28
          md:w-32
          md:h-32
          border-4 border-lightest
          dark:border-black
          bg-black
        "
        style="margin-top: 6rem"
      >
        <img v-lazy="profile.photoURL" class="w-28 h-28 md:w-32 md:h-32" />
      </div>
    </div>
    <div class="mt-5 px-6">
      <div class="w-full flex flex-col space-y-4">
        <div class="w-full block mt-4">
          <h1 class="text-2xl font-bold dark:text-lightest">
            {{ profile.name }}
          </h1>
          <h2 class="dark:text-gray">@{{ profile.handle }}</h2>
        </div>
        <p class="w-full dark:text-lightest">
          {{ profile.bio }}
        </p>
        <div
          class="
            w-full
            flex flex-wrap flex-col
            md:flex-row
            md:space-x-4
            text-sm
          "
        >
          <div
            v-show="profile.location !== ''"
            class="flex items-center space-x-1 dark:text-gray"
          >
            <IconMapMarker />
            <p>{{ profile.location }}</p>
          </div>
          <div
            v-show="profile.website !== ''"
            class="flex items-center space-x-1 dark:text-gray"
          >
            <IconLink />
            <a
              :href="profile.website"
              target="_blank"
              rel="noreferrer noopener"
              class="text-blue hover:underline"
            >
              {{ profile.website }}
            </a>
          </div>
          <div
            v-show="validBirthDate"
            class="flex items-center space-x-1 dark:text-gray"
          >
            <IconGift />
            <p>Born {{ parsedBirthDate }}</p>
          </div>
          <div class="flex items-center space-x-1 dark:text-gray">
            <IconCalendar />
            <p>Joined {{ parsedJoinedAt }}</p>
          </div>
        </div>
        <div
          class="
            w-full
            flex flex-wrap flex-col
            md:flex-row
            md:space-x-4
            text-sm
          "
        >
          <div class="flex items-center space-x-2">
            <p class="font-bold dark:text-lightest">
              {{ profile.followingsCount }}
            </p>
            <p class="dark:text-gray">Following</p>
          </div>
          <div class="flex items-center space-x-2">
            <p class="font-bold dark:text-lightest">
              {{ profile.followersCount }}
            </p>
            <p class="dark:text-gray">Followers</p>
          </div>
        </div>
      </div>
    </div>
    <div
      class="
        w-full
        flex
        justify-between
        items-center
        mt-4
        border-b border-lighter
        dark:border-dark
      "
    >
    </div>

    <div v-show="!initialLoadDone" class="flex flex-col">
      <div class="w-full text-center">
        <LoadingSpinner />
      </div>
    </div>
    <div v-show="initialLoadDone" class="flex flex-col">
      <div v-for="tweet in tweets" :key="tweet.id_str">
        <TweetCard v-if="!tweet.isReply" :tweet="tweet" />
        <TweetConversationCard v-else :tweet="tweet" />
      </div>

      <div
        v-show="tweets.length > 0 && loadNextBatch"
        class="
          w-full
          p-4
          border-b border-lighter
          dark:border-dark
          hover:bg-lighter
          dark:hover:bg-darker
          flex
          cursor-pointer
        "
      >
        <div class="w-full text-center">
          <LoadingSpinner />
        </div>
      </div>
    </div>
  </main>
</template>
