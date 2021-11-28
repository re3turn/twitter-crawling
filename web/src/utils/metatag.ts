import {Tweet} from "../modules/tweets/types";
import {ProfileDetails} from "../modules/user/types";

export function tweetMetaTag(tweet: Tweet & {replies: Tweet[]}, metaData: any) {
    metaData.title = `${tweet?.authorName} @${tweet?.authorHandle}`
    metaData.meta = [
        {property: 'og:title', content: `${tweet?.authorName} @${tweet?.authorHandle}`},
        {property: 'og:description', content: `${tweet?.content}`},
        {property: 'og:type', content: 'website'},
        {property: 'og:url', content: location.href},
        {property: 'og:site_name', content: 'tweet'},
        {property: 'robots', content: 'noindex, nofollow'},
        {property: 'referrer', content: 'no-referrer'},
    ]
}

export function userMetaTag(user: ProfileDetails, metaData: any) {
    metaData.title = `${user.name} @${user.handle}`
    metaData.meta = [
        {property: 'og:title', content: `${user.name} @${user.handle}`},
        {property: 'og:description', content: `${user.bio}`},
        {property: 'og:type', content: 'website'},
        {property: 'og:url', content: location.href},
        {property: 'og:site_name', content: 'tweet'},
        {property: 'robots', content: 'noindex, nofollow'},
        {property: 'referrer', content: 'no-referrer'},
    ]
}