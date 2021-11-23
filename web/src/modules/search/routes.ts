import { RouteRecordRaw } from 'vue-router'
import BaseLayout from '../../modules/layouts/BaseLayout.vue'
import { makeRoutesWithLayout } from '../../utils/routes'

const routes: RouteRecordRaw[] = [
  {
    path: '',
    component: () => import('./index.vue'),
  },
]

export default makeRoutesWithLayout('/search', BaseLayout, routes)
