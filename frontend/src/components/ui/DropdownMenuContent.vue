<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String,
  align: {
    type: String,
    default: 'end'
  }
})

const alignClass = {
  start: 'left-0',
  center: 'left-1/2 -translate-x-1/2',
  end: 'right-0'
}

const contentClass = computed(() =>
  cn(
    'absolute z-50 mt-2 min-w-[8rem] overflow-hidden rounded-md border border-slate-200 bg-white p-1 text-slate-950 shadow-md animate-in fade-in-80',
    alignClass[props.align],
    props.class
  )
)
</script>

<template>
  <div :class="contentClass">
    <slot />
  </div>
</template>
