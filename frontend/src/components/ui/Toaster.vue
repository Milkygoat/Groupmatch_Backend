<script setup>
import { computed } from 'vue'
import { useToast } from '@/composables/useToast'
import { X, CheckCircle, AlertCircle, Info } from 'lucide-vue-next'

const { toasts, removeToast } = useToast()

const getIcon = (variant) => {
  switch (variant) {
    case 'destructive':
      return AlertCircle
    case 'success':
      return CheckCircle
    default:
      return Info
  }
}

const getVariantClasses = (variant) => {
  switch (variant) {
    case 'destructive':
      return 'bg-red-50 border-red-200 text-red-800'
    case 'success':
      return 'bg-green-50 border-green-200 text-green-800'
    default:
      return 'bg-white border-slate-200 text-slate-800'
  }
}
</script>

<template>
  <div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'rounded-lg border p-4 shadow-lg',
          getVariantClasses(toast.variant)
        ]"
      >
        <div class="flex items-start gap-3">
          <component
            :is="getIcon(toast.variant)"
            :class="[
              'h-5 w-5 flex-shrink-0',
              toast.variant === 'destructive' ? 'text-red-500' :
              toast.variant === 'success' ? 'text-green-500' :
              'text-cyan-500'
            ]"
          />
          <div class="flex-1">
            <p v-if="toast.title" class="text-sm font-semibold">{{ toast.title }}</p>
            <p v-if="toast.description" class="text-sm opacity-80 mt-1">{{ toast.description }}</p>
          </div>
          <button
            @click="removeToast(toast.id)"
            class="flex-shrink-0 rounded-md p-1 hover:bg-black/10 transition-colors"
          >
            <X class="h-4 w-4" />
          </button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>
