<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String
})

const descClass = computed(() =>
  cn('text-sm text-slate-500', props.class)
)
</script>

<template>
  <p :class="descClass">
    <slot />
  </p>
</template>
