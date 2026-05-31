<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String,
  value: String
})

const emit = defineEmits(['select'])

const itemClass = computed(() =>
  cn(
    'relative flex w-full cursor-pointer select-none items-center rounded-sm py-2 px-3 text-sm outline-none hover:bg-slate-100 focus:bg-slate-100',
    props.class
  )
)
</script>

<template>
  <div
    :class="itemClass"
    @click="$emit('select', value)"
  >
    <slot />
  </div>
</template>
