<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String,
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'secondary', 'destructive', 'outline'].includes(v)
  }
})

const variants = {
  default: 'border-transparent bg-slate-900 text-slate-50 hover:bg-slate-900/80',
  secondary: 'border-transparent bg-slate-100 text-slate-900 hover:bg-slate-100/80',
  destructive: 'border-transparent bg-red-500 text-slate-50 hover:bg-red-500/80',
  outline: 'text-slate-950 border-slate-200'
}

const badgeClass = computed(() =>
  cn(
    'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2',
    variants[props.variant],
    props.class
  )
)
</script>

<template>
  <div :class="badgeClass">
    <slot />
  </div>
</template>
