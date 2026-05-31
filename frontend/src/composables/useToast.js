import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
  const toast = ({ title, description, variant = 'default', duration = 4000 }) => {
    const id = ++toastId
    const newToast = {
      id,
      title,
      description,
      variant,
    }
    
    toasts.value.push(newToast)
    
    // Auto remove after duration
    setTimeout(() => {
      removeToast(id)
    }, duration)
    
    return id
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  return {
    toasts,
    toast,
    removeToast
  }
}
