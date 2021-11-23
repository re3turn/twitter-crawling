<template>
  <div v-if="media.mediaType == 'video'" class="player-container" :class="clazz">
    <vue3-video-player :src="media.url"></vue3-video-player>
  </div>
  <img v-else
      v-lazy="media.url"
      :class="clazz"
  />
</template>

<script lang="ts">
import {Media} from "../modules/tweets/types";
import {defineComponent} from "vue";

export default defineComponent( {
  name: "MediaContent",
  props: {
    media: {
      type: Object as () => Media,
      required: true,
    },
    clazz: {
      type: String
    }
  },
})
</script>
