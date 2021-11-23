import { createApp } from 'vue'
import { Lazyload } from '@vant/lazyload'

import { router } from './routes'
import { store } from './store'
import { createMetaManager } from 'vue-meta'
import Vue3VideoPlayer from '@cloudgeek/vue3-video-player'
import '@cloudgeek/vue3-video-player/dist/vue3-video-player.css'

import './assets/styles/root.css'
import App from './App.vue'

const app = createApp(App)

app.use(Vue3VideoPlayer, {
    lang: 'en'
})
app.use(createMetaManager())
app.use(store)
app.use(router)
app.use(Lazyload)
app.mount('#app')
