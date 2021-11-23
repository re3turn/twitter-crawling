<script lang="ts">
import { defineComponent, resolveComponent, h, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from './store'
import axios from './utils/axios'
import { Action } from './modules/storeActionTypes'
import { Theme } from './modules/theme/types'
import { useMeta } from 'vue-meta'

export default defineComponent({
  setup() {
    const store = useStore()
    const router = useRouter()
    const RouterView = resolveComponent('router-view')
    useMeta({
      title: '',
      meta: [
        {property: 'robots', content: 'noindex, nofollow'},
      ]
    })

    const responseInterceptor = axios.interceptors.response.use(
      (res) => res,
      async (error) => {
        if (error.response.status === 401) {
          axios.interceptors.response.eject(responseInterceptor)
        }
      }
    )

    onMounted(() => {
      document.querySelector('body')?.classList.add('bg-white', 'dark:bg-black')
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        window.localStorage.setItem('theme', 'dark')
        store.dispatch(Action.ThemeActionTypes.TOGGLE_THEME, 'dark')
        document.querySelector('html')?.classList.add('dark')
      } else {
        window.localStorage.setItem('theme', 'dark')
        store.dispatch(Action.ThemeActionTypes.TOGGLE_THEME, 'light')
        document.querySelector('html')?.classList.remove('dark')
      }

      watch(
        () => store.getters['currentTheme'],
        (theme) => {
          store.dispatch(Action.ThemeActionTypes.TOGGLE_THEME, theme as Theme)

          if (store.getters['currentTheme'] === 'dark') {
            document.querySelector('html')?.classList.add('dark')
          } else {
            document.querySelector('html')?.classList.remove('dark')
          }
        }
      )
    })

    return () => h(RouterView)
  },
})
</script>
