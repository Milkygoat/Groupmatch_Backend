<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String
})

const scrollClass = computed(() =>
  cn('relative overflow-auto max-h-[300px]', props.class)
)
</script>

<template>
  <div :class="scrollClass">
    <slot />
  </div>
</template>
