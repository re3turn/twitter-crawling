<script lang="ts">
import { computed, defineComponent, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import IconSearch from '../../icons/IconSearch.vue'

export default defineComponent({
  components: { IconSearch },
  name: 'TrendingSidebar',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const searchFocused = ref(false)
    const searchQuery = ref('')

    const isInSearchPage = computed(() => route.path === '/search')

    function redirectWithSearchQuery() {
      router.push({
        path: '/search',
        query: { q: searchQuery.value },
      })
      return
    }

    return {
      searchFocused,
      searchQuery,
      redirectWithSearchQuery,
      isInSearchPage,
    }
  },
})
</script>

<template>
  <div
    class="
      md:block
      hidden
      w-1/2
      h-full
      border-l border-lighter
      dark:border-dark
      py-2
      px-6
      overflow-y-scroll
      relative
    "
  >
    <form v-show="!isInSearchPage" @submit.prevent="redirectWithSearchQuery">
      <input
        class="
          pl-12
          rounded-full
          w-full
          p-3
          bg-lighter
          dark:bg-darkest
          dark:text-light
          text-sm
          mb-4
          focus:bg-white
          dark:focus:bg-black
          focus:outline-none
          border-2 border-lighter
          dark:border-darkest
          focus:border-blue
          dark:focus:border-blue
          dark:focus:text-lightest
          transition
          duration-150
        "
        @focus="searchFocused = true"
        @blur="searchFocused = false"
        v-model="searchQuery"
        type="search"
        placeholder="Search Twitter"
      />
      <IconSearch
        :size="24"
        class="absolute left-0 top-0 mt-5 ml-10"
        :class="searchFocused ? 'text-blue' : 'text-light'"
      />
      <input type="submit" class="hidden" />
    </form>
  </div>
</template>
