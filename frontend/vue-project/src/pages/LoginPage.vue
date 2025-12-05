<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-lg space-y-6">
      <h2 class="text-3xl font-bold text-indigo-700 text-center">로그인</h2>
      <p class="text-center text-gray-500">실시간 맞춤형 뉴스 큐레이션 서비스</p>
      <div>
        <label for="login-username" class="block text-sm font-medium text-gray-700 mb-1">사용자 이름</label>
        <input id="login-username" type="text" placeholder="UserA"
               class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800"
               v-model="loginForm.username" />
      </div>
      <div>
        <label for="login-password" class="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
        <input id="login-password" type="password" placeholder="********"
               class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800"
               v-model="loginForm.password" />
      </div>
      <button @click="handleLogin" class="w-full bg-indigo-600 text-white p-3 rounded-lg font-semibold hover:bg-indigo-700 transition">
        로그인 (Django API 연동)
      </button>
      <p class="text-center text-sm text-gray-600">
        계정이 없으신가요?
        <a @click="$emit('go-to-register')" class="text-indigo-600 hover:text-indigo-800 font-medium cursor-pointer">회원가입</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';

const emit = defineEmits(['go-to-register', 'login-success']);
const router = useRouter();
const userStore = useUserStore();

const loginForm = ref({ username: 'UserA', password: '123' });

const handleLogin = () => {
  // Development-only simulation before backend is connected
  console.log(`[Django API 호출 - 시뮬레이션]: 사용자 ${loginForm.value.username} 로그인 시도...`);
  userStore.loginSimulate(loginForm.value.username);
  router.push({ name: 'main' });
  emit('login-success');
};
</script>