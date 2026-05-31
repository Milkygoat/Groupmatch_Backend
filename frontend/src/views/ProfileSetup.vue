<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { ROLES } from '@/mock/mockData'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Badge from '@/components/ui/Badge.vue'
import Avatar from '@/components/ui/Avatar.vue'
import AvatarImage from '@/components/ui/AvatarImage.vue'
import AvatarFallback from '@/components/ui/AvatarFallback.vue'
import Select from '@/components/ui/Select.vue'
import SelectItem from '@/components/ui/SelectItem.vue'
import { User, Calendar, Briefcase, Tag, X, Camera, UserCircle } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const { toast } = useToast()

const fileInputRef = ref(null)
const isSubmitting = ref(false)
const loading = ref(false)

const formData = ref({
  username: '',
  name: '',
  birthdate: '',
  role: '',
  skills: [],
  avatar: ''
})

const avatarFile = ref(null)
const skillInput = ref('')

onMounted(() => {
  if (authStore.user) {
    formData.value = {
      username: authStore.user.username || '',
      name: authStore.user.name || '',
      birthdate: authStore.user.birthdate || '',
      role: authStore.user.role || '',
      skills: authStore.user.skills || [],
      avatar: authStore.user.avatar || ''
    }
  }
})

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      toast({
        title: 'File terlalu besar',
        description: 'Maksimal ukuran file adalah 2MB',
        variant: 'destructive'
      })
      return
    }

    avatarFile.value = file

    const reader = new FileReader()
    reader.onloadend = () => {
      formData.value.avatar = reader.result
    }
    reader.readAsDataURL(file)
  }
}

const handleAddSkill = () => {
  if (skillInput.value.trim() && !formData.value.skills.includes(skillInput.value.trim())) {
    formData.value.skills.push(skillInput.value.trim())
    skillInput.value = ''
  }
}

const handleRemoveSkill = (skillToRemove) => {
  formData.value.skills = formData.value.skills.filter(skill => skill !== skillToRemove)
}

const handleSubmit = async () => {
  if (isSubmitting.value) return

  if (!formData.value.username || !formData.value.name || !formData.value.birthdate || !formData.value.role || formData.value.skills.length === 0) {
    toast({
      title: 'Data tidak lengkap',
      description: 'Silakan lengkapi semua field.',
      variant: 'destructive'
    })
    return
  }

  isSubmitting.value = true
  loading.value = true

  try {
    // 1. CREATE PROFILE DULU (TANPA AVATAR)
    await authStore.updateProfile({
      username: formData.value.username,
      name: formData.value.name,
      birthdate: formData.value.birthdate,
      role: formData.value.role,
      skills: formData.value.skills
    })

    // 2. BARU upload avatar (JIKA ADA)
    if (avatarFile.value) {
      const uploadResponse = await authStore.uploadAvatar(avatarFile.value)
      console.log('Avatar uploaded:', uploadResponse.avatar_url)
    }

    toast({
      title: 'Profil berhasil disimpan!',
      description: 'Anda dapat mulai mencari tim.'
    })

    router.push('/dashboard')
  } catch (error) {
    console.error('Profile update failed:', error)

    toast({
      title: 'Gagal Menyimpan',
      description: error.response?.data?.detail || 'Terjadi kesalahan saat menyimpan profil.',
      variant: 'destructive'
    })

    isSubmitting.value = false
    loading.value = false
  }
}

const selectRole = (value) => {
  formData.value.role = value
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-cyan-50 via-white to-teal-50 px-4 py-8">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 right-20 w-64 h-64 bg-cyan-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20"></div>
      <div class="absolute bottom-20 left-20 w-64 h-64 bg-teal-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20"></div>
    </div>

    <Card class="w-full max-w-2xl shadow-xl border-0 bg-white/90 backdrop-blur-sm rounded-2xl relative z-10">
      <CardHeader class="space-y-3 text-center pb-6">
        <div class="mx-auto mb-2">
          <div class="w-14 h-14 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto">
            <UserCircle class="h-7 w-7 text-white" />
          </div>
        </div>
        <h1 class="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent">GroupMatch</h1>
        <CardTitle class="text-xl font-bold text-slate-800">Lengkapi Profilmu</CardTitle>
        <CardDescription class="text-slate-500">
          Informasi ini membantu kami menemukan tim yang tepat untukmu
        </CardDescription>
      </CardHeader>

      <CardContent class="px-6 pb-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Upload Foto Profil -->
          <div class="flex flex-col items-center justify-center mb-6">
            <div
              class="relative cursor-pointer group"
              @click="fileInputRef?.click()"
            >
              <Avatar class="h-24 w-24 border-4 border-white shadow-md">
                <AvatarImage :src="formData.avatar" alt="Profile" class="object-cover" />
                <AvatarFallback class="text-2xl bg-cyan-100 text-cyan-600">
                  {{ formData.name ? formData.name.charAt(0).toUpperCase() : 'U' }}
                </AvatarFallback>
              </Avatar>

              <!-- Overlay Edit -->
              <div class="absolute inset-0 flex items-center justify-center bg-black/40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                <Camera class="h-8 w-8 text-white" />
              </div>

              <!-- Tombol Kamera Kecil -->
              <div class="absolute bottom-0 right-0 bg-cyan-500 rounded-full p-2 border-2 border-white shadow-sm group-hover:scale-110 transition-transform">
                <Camera class="h-4 w-4 text-white" />
              </div>
            </div>
            <p class="text-sm text-slate-500 mt-2">Klik untuk mengubah foto</p>

            <!-- Hidden Input File -->
            <input
              type="file"
              ref="fileInputRef"
              class="hidden"
              accept="image/*"
              @change="handleImageUpload"
            />
          </div>

          <div class="space-y-2">
            <Label for="username" class="text-slate-700">Username</Label>
            <div class="relative">
              <User class="absolute left-3 top-3 h-4 w-4 text-slate-400" />
              <Input
                id="username"
                type="text"
                placeholder="Buat username unik Anda (contoh: johndoe)"
                class="pl-10 bg-slate-50 border-slate-200 focus:ring-cyan-500 focus:border-cyan-500 rounded-lg"
                v-model="formData.username"
                required
              />
            </div>
          </div>

          <div class="space-y-2">
            <Label for="name" class="text-slate-700">Nama Lengkap</Label>
            <div class="relative">
              <User class="absolute left-3 top-3 h-4 w-4 text-slate-400" />
              <Input
                id="name"
                type="text"
                placeholder="Nama lengkap Anda"
                class="pl-10 bg-slate-50 border-slate-200 focus:ring-cyan-500 focus:border-cyan-500 rounded-lg"
                v-model="formData.name"
                required
              />
            </div>
          </div>

          <div class="space-y-2">
            <Label for="birthdate" class="text-slate-700">Tanggal Lahir</Label>
            <div class="relative">
              <Calendar class="absolute left-3 top-3 h-4 w-4 text-slate-400" />
              <Input
                id="birthdate"
                type="date"
                class="pl-10 bg-slate-50 border-slate-200 focus:ring-cyan-500 focus:border-cyan-500 rounded-lg"
                v-model="formData.birthdate"
                required
              />
            </div>
          </div>

          <div class="space-y-2">
            <Label for="role" class="text-slate-700">Role</Label>
            <div class="relative">
              <Briefcase class="absolute left-3 top-3 h-4 w-4 text-slate-400 z-10" />
              <Select
                v-model="formData.role"
                placeholder="Pilih role Anda"
                class="pl-10"
              >
                <template #default="{ selectOption }">
                  <SelectItem
                    v-for="role in ROLES"
                    :key="role.value"
                    :value="role.value"
                    @select="selectOption(role.value)"
                  >
                    <div class="flex items-center gap-2">
                      <div :class="`w-3 h-3 rounded-full ${role.color}`"></div>
                      {{ role.label }}
                    </div>
                  </SelectItem>
                </template>
              </Select>
            </div>
          </div>

          <div class="space-y-2">
            <Label for="skills" class="text-slate-700">Skills</Label>
            <div class="space-y-3">
              <div class="flex gap-2">
                <div class="relative flex-1">
                  <Tag class="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input
                    id="skills"
                    type="text"
                    placeholder="Tambah skill (contoh: Vue, Python)"
                    class="pl-10 bg-slate-50 border-slate-200 focus:ring-cyan-500 focus:border-cyan-500 rounded-lg"
                    v-model="skillInput"
                    @keypress.enter.prevent="handleAddSkill"
                  />
                </div>
                <Button
                  type="button"
                  @click="handleAddSkill"
                  class="border-2 border-slate-200 text-slate-600 hover:border-slate-300 hover:text-slate-700 hover:bg-slate-100 bg-transparent rounded-lg font-medium transition-colors"
                >
                  Tambah
                </Button>
              </div>

              <div v-if="formData.skills.length > 0" class="flex flex-wrap gap-2 p-3 bg-cyan-50 border border-cyan-100 rounded-lg">
                <Badge
                  v-for="(skill, index) in formData.skills"
                  :key="index"
                  class="bg-slate-100 text-slate-600 rounded-full px-3 py-1 text-sm"
                >
                  {{ skill }}
                  <button
                    type="button"
                    @click="handleRemoveSkill(skill)"
                    class="ml-2 hover:text-red-600"
                  >
                    <X class="h-3 w-3" />
                  </button>
                </Badge>
              </div>
            </div>
          </div>

          <Button
            type="submit"
            class="w-full bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg shadow-sm font-medium"
            :disabled="loading"
          >
            {{ loading ? 'Menyimpan...' : 'Simpan Profil' }}
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
