<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String
})

const cardClass = computed(() =>
  cn(
    'rounded-lg border border-slate-200 bg-white text-slate-950 shadow-sm',
    props.class
  )
)
</script>

<template>
  <div :class="cardClass">
    <slot />
  </div>
</template>
