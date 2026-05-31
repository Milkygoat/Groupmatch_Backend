<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String
})

const isOpen = ref(false)

const menuClass = computed(() =>
  cn('relative inline-block text-left', props.class)
)

const close = () => {
  isOpen.value = false
}

const toggle = () => {
  isOpen.value = !isOpen.value
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.dropdown-menu')) {
    close()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

defineExpose({ isOpen, toggle, close })
</script>

<template>
  <div :class="menuClass" class="dropdown-menu">
    <slot :is-open="isOpen" :toggle="toggle" :close="close" />
  </div>
</template>
