<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String,
  disabled: Boolean
})

const emit = defineEmits(['click'])

const itemClass = computed(() =>
  cn(
    'relative flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors hover:bg-slate-100 focus:bg-slate-100',
    props.disabled && 'pointer-events-none opacity-50',
    props.class
  )
)
</script>

<template>
  <div
    :class="itemClass"
    @click="$emit('click', $event)"
  >
    <slot />
  </div>
</template>
