import { GuardContext } from '../types'

export default async function (ctx: GuardContext) {
  ctx.next()
}
