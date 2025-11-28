<template>
<div class="space-y-8 bg-white p-8 rounded-xl shadow-lg">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">⚙️ 마이페이지 (관심 분야 및 활동 관리)</h2>

    <!-- 탭 메뉴 -->
    <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
            <button @click="mypageTab = 'topics'" :class="{'active-tab': mypageTab === 'topics', 'text-gray-500 hover:text-gray-700': mypageTab !== 'topics'}" class="whitespace-nowrap py-3 px-1 font-medium text-sm transition">
                관심 분야 설정
            </button>
            <button @click="mypageTab = 'activity'" :class="{'active-tab': mypageTab === 'activity', 'text-gray-500 hover:text-gray-700': mypageTab !== 'activity'}" class="whitespace-nowrap py-3 px-1 font-medium text-sm transition">
                활동 기록 관리
            </button>
        </nav>
    </div>

    <!-- 탭 콘텐츠 -->
    <div class="mt-6">
        
        <!-- 6.1. 관심 분야 설정 탭 -->
        <div v-if="mypageTab === 'topics'" class="space-y-6">
            <h3 class="text-xl font-semibold text-gray-700">관심 분야 수정</h3>
            <p class="text-sm text-gray-500">선택한 분야에 따라 뉴스 피드의 **맞춤 추천** 결과가 달라집니다.</p>

            <div>
                <div class="flex flex-wrap gap-2">
                    <button v-for="topic in availableTopics" :key="topic"
                            @click="toggleTopic(topic)"
                            :class="{'bg-indigo-600 text-white ring-2 ring-indigo-800': selectedTopics.includes(topic), 
                                     'bg-gray-100 text-gray-700 hover:bg-indigo-100 hover:text-indigo-600 border border-gray-300': !selectedTopics.includes(topic)}"
                            class="px-4 py-2 rounded-full font-medium text-sm transition duration-150 ease-in-out">
                        {{ topic }}
                    </button>
                </div>
                <p class="text-xs text-gray-500 mt-3">현재 설정된 분야: <span class="font-semibold text-indigo-700">{{ selectedTopics.join(', ') }}</span></p>
            </div>

            <button @click="handleUpdateTopics" class="w-full max-w-md bg-indigo-600 text-white p-3 rounded-lg font-semibold hover:bg-indigo-700 transition">
                관심 분야 업데이트 (PostgreSQL 반영)
            </button>
        </div>

        <!-- 6.2. 활동 기록 관리 탭 (선택 삭제 기능 구현) -->
        <div v-else-if="mypageTab === 'activity'" class="space-y-6">
            <h3 class="text-xl font-semibold text-gray-700 mb-4">활동 데이터 관리</h3>
            <p class="text-sm text-gray-500">개별 기록을 삭제할 수 있으며, 이는 대시보드 및 추천 로직에 즉시 반영됩니다.</p>

            <!-- 좋아요 기록 목록 및 개별 삭제 -->
            <div class="border p-4 rounded-xl space-y-3">
                <h4 class="font-medium text-lg text-gray-800">❤️ 좋아요한 기사 (총 {{ likedArticlesList.length }}건)</h4>
                <ul class="space-y-2 max-h-64 overflow-y-auto">
                    <li v-for="article in likedArticlesList" :key="article.id"
                        class="flex justify-between items-center bg-white p-2 rounded border border-gray-100">
                        <span class="flex-grow truncate pr-2 text-sm cursor-pointer hover:text-indigo-600" @click="$emit('select-article', article)">
                            {{ article.title }}
                        </span>
                        <button @click="$emit('delete-like', article.id)"
                            class="text-red-500 hover:text-red-700 text-xs font-semibold p-1 transition flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                            삭제
                        </button>
                    </li>
                    <li v-if="likedArticlesList.length === 0" class="text-gray-500 text-center py-4">좋아요한 기사가 없습니다.</li>
                </ul>
            </div>

            <!-- 읽은 기록 목록 및 개별 삭제 -->
            <div class="border p-4 rounded-xl space-y-3">
                <h4 class="font-medium text-lg text-gray-800">📚 최근 읽은 기록 (총 {{ readArticles.length }}건)</h4>
                <ul class="space-y-2 max-h-64 overflow-y-auto">
                    <li v-for="(read, index) in readArticles" :key="read.read_at + read.id + index"
                        class="flex justify-between items-center bg-white p-2 rounded border border-gray-100">
                        <span class="flex-grow truncate pr-2 text-sm cursor-pointer hover:text-indigo-600" @click="$emit('select-article-by-id', read.id)">
                            [{{ read.read_at.split(' ')[0] }}] {{ read.title }}
                        </span>
                        <button @click="$emit('delete-read', index)"
                            class="text-red-500 hover:text-red-700 text-xs font-semibold p-1 transition flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                            삭제
                        </button>
                    </li>
                    <li v-if="readArticles.length === 0" class="text-gray-500 text-center py-4">읽은 기록이 없습니다.</li>
                </ul>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
    currentUser: Object,
    availableTopics: Array,
    likedArticlesList: Array,
    readArticles: Array
});

const emit = defineEmits(['update-topics', 'delete-like', 'delete-read', 'select-article-by-id', 'select-article']);

const mypageTab = ref('topics'); // 내부 탭 상태
const selectedTopics = ref([]);

// 컴포넌트 초기화 시 현재 사용자의 관심사를 가져옴
watch(() => props.currentUser.keywords, (newKeywords) => {
    selectedTopics.value = newKeywords.split(', ').filter(k => k);
}, { immediate: true });


const toggleTopic = (topic) => {
    const index = selectedTopics.value.indexOf(topic);
    if (index === -1) {
        selectedTopics.value.push(topic);
    } else {
        selectedTopics.value.splice(index, 1);
    }
};

const handleUpdateTopics = () => {
    // App.vue의 updateTopics 함수를 호출하여 상태를 중앙에서 변경하도록 요청
    emit('update-topics', selectedTopics.value);
};
</script>