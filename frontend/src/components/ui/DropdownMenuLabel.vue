<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String
})

const labelClass = computed(() =>
  cn('px-2 py-1.5 text-sm font-semibold', props.class)
)
</script>

<template>
  <div :class="labelClass">
    <slot />
  </div>
</template>
