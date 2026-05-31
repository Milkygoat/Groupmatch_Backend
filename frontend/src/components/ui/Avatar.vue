<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String,
  src: String,
  alt: String
})

const avatarClass = computed(() =>
  cn(
    'relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full',
    props.class
  )
)
</script>

<template>
  <span :class="avatarClass">
    <slot />
  </span>
</template>
