<template>
<div class="flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-lg space-y-6">
        <h2 class="text-3xl font-bold text-indigo-700 text-center">회원가입</h2>
        <p class="text-center text-gray-500">PostgreSQL에 사용자 정보가 저장됩니다.</p>
        
        <!-- 생략된 입력 필드: username, password -->
        
        <!-- 관심 분야 선택 (버튼/태그 형식) -->
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">관심 분야 선택 (규칙 기반 큐레이션)</label>
            <div class="flex flex-wrap gap-2">
                <button v-for="topic in availableTopics" :key="topic"
                        @click="toggleTopic(topic)"
                        :class="{'bg-indigo-600 text-white ring-2 ring-indigo-800': selectedTopics.includes(topic), 
                                 'bg-gray-100 text-gray-700 hover:bg-indigo-100 hover:text-indigo-600 border border-gray-300': !selectedTopics.includes(topic)}"
                        class="px-4 py-2 rounded-full font-medium text-sm transition duration-150 ease-in-out">
                    {{ topic }}
                </button>
            </div>
            <p class="text-xs text-gray-500 mt-2">선택된 분야: <span class="font-semibold">{{ selectedTopics.join(', ') }}</span></p>
        </div>
        
        <button @click="handleRegister" class="w-full bg-indigo-600 text-white p-3 rounded-lg font-semibold hover:bg-indigo-700 transition">
            회원가입 완료 (Django API 연동)
        </button>
        <p class="text-center text-sm text-gray-600">
            <a @click="$emit('go-to-login')" class="text-indigo-600 hover:text-indigo-800 font-medium cursor-pointer">로그인 페이지로 돌아가기</a>
        </p>
    </div>
</div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    availableTopics: Array // App.vue에서 전달받음
});
const emit = defineEmits(['go-to-login', 'register-success']);

const registerForm = ref({
    username: '',
    password: ''
});
const selectedTopics = ref([]);

const toggleTopic = (topic) => {
    const index = selectedTopics.value.indexOf(topic);
    if (index === -1) {
        selectedTopics.value.push(topic);
    } else {
        selectedTopics.value.splice(index, 1);
    }
};

const handleRegister = () => {
    if (selectedTopics.value.length === 0) {
        alert("관심 분야를 최소 하나 이상 선택해주세요.");
        return;
    }
    
    // --- API 연동 로직이 들어갈 곳 ---
    console.log(`[Django API 호출]: 사용자 등록 및 관심 분야 저장: ${selectedTopics.value.join(', ')}`);
    
    // 시뮬레이션 성공 시
    alert(`회원가입이 완료되었습니다!`);
    emit('register-success'); // go-to-login을 트리거
};
</script>