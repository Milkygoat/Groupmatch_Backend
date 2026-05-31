<script setup>
import { ref, computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String,
  src: String,
  alt: String
})

const hasError = ref(false)

const imageClass = computed(() =>
  cn('aspect-square h-full w-full object-cover', props.class)
)

const handleError = () => {
  hasError.value = true
}
</script>

<template>
  <img
    v-if="src && !hasError"
    :class="imageClass"
    :src="src"
    :alt="alt"
    @error="handleError"
  />
</template>
