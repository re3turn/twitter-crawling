import { createRouter, createWebHistory } from 'vue-router'
import { store } from './store'
import routes from './modules/routes'

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

