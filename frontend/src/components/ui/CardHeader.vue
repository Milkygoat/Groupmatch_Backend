<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String
})

const headerClass = computed(() =>
  cn('flex flex-col space-y-1.5 p-6', props.class)
)
</script>

<template>
  <div :class="headerClass">
    <slot />
  </div>
</template>
