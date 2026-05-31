<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String
})

const fallbackClass = computed(() =>
  cn(
    'flex h-full w-full items-center justify-center rounded-full bg-slate-100',
    props.class
  )
)
</script>

<template>
  <span :class="fallbackClass">
    <slot />
  </span>
</template>
