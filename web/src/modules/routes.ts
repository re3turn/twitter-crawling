import userRoutes from './user/routes'
import searchRoutes from './search/routes'
import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  searchRoutes,
  userRoutes,
]

export default routes
