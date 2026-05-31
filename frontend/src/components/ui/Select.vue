<script setup>
import { ref, computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: String,
  modelValue: String,
  placeholder: String,
  disabled: Boolean
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)

const triggerClass = computed(() =>
  cn(
    'flex h-10 w-full items-center justify-between rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
    props.class
  )
)

const toggleOpen = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value
  }
}

const selectOption = (value) => {
  emit('update:modelValue', value)
  isOpen.value = false
}

defineExpose({ isOpen, selectOption })
</script>

<template>
  <div class="relative">
    <button
      type="button"
      :class="triggerClass"
      :disabled="disabled"
      @click="toggleOpen"
    >
      <span v-if="modelValue">{{ modelValue }}</span>
      <span v-else class="text-slate-500">{{ placeholder }}</span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="h-4 w-4 opacity-50"
      >
        <path d="m6 9 6 6 6-6" />
      </svg>
    </button>
    
    <div
      v-if="isOpen"
      class="absolute z-50 mt-1 w-full rounded-md border border-slate-200 bg-white shadow-md"
    >
      <slot :select-option="selectOption" />
    </div>
  </div>
</template>
