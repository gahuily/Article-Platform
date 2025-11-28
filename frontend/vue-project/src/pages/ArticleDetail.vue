<template>
<div class="bg-white p-8 rounded-xl shadow-lg space-y-6">
    <button @click="$emit('go-to-main')" class="text-indigo-600 hover:text-indigo-800 font-semibold mb-4 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        목록으로 돌아가기
    </button>

    <h2 class="text-3xl font-extrabold text-gray-900">{{ selectedArticle.title }}</h2>
    <p class="text-sm text-gray-500 border-b pb-4">
        발행: {{ selectedArticle.published_at }} | 출처: **{{ selectedArticle.source }}**
    </p>
    
    <!-- 기사 본문 -->
    <div class="prose max-w-none text-gray-700 leading-relaxed">
        <p class="font-semibold text-lg text-indigo-700 mb-4">{{ selectedArticle.summary }}</p>
        <p> {{ selectedArticle.content }} </p>
    </div>
    
    <!-- 관련 기사 추천 (2개) -->
    <div class="bg-yellow-50 p-4 rounded-xl border border-yellow-300">
        <h3 class="text-lg font-bold text-yellow-800 mb-3 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            함께 볼 만한 추천 기사 ({{ getMainTopic(selectedArticle) }} 분야)
        </h3>
        <div class="space-y-2">
            <div v-for="article in relatedArticles" :key="article.id"
                 @click="$emit('select-article', article)"
                 class="p-2 bg-white rounded-lg hover:bg-yellow-100 cursor-pointer transition">
                <p class="text-sm font-medium text-gray-800 line-clamp-1">{{ article.title }}</p>
                <p class="text-xs text-gray-500">{{ article.summary }}</p>
            </div>
            <p v-if="relatedArticles.length === 0" class="text-xs text-gray-500">이 분야에 추천할 다른 기사가 없습니다.</p>
        </div>
    </div>


    <!-- 좋아요 및 원문 보기 (아이콘과 카운트 동적 구현) -->
    <div class="flex justify-between items-center pt-4 border-t">
        <button @click="$emit('toggle-like', selectedArticle)"
                :class="{'bg-red-500 hover:bg-red-600': selectedArticle.isLiked, 'bg-gray-300 hover:bg-gray-400': !selectedArticle.isLiked}"
                class="text-white px-6 py-3 rounded-lg font-bold transition flex items-center space-x-2">
            <svg v-if="selectedArticle.isLiked" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            <span>{{ selectedArticle.likes }}</span>
        </button>
        <a :href="selectedArticle.link" target="_blank" class="text-indigo-600 hover:text-indigo-800 font-semibold transition">
            원문 링크 보기 &rarr;
        </a>
    </div>

    <!-- AI 기반 챗봇 -->
    <div class="mt-8 p-6 bg-indigo-50 rounded-xl border-t-4 border-green-500">
        <h3 class="text-xl font-bold text-green-700 mb-4">🤖 기사 기반 AI 챗봇</h3>
        <p class="text-sm text-gray-600 mb-4">* 이 기사 내용에 대해 질문해보세요. (Elasticsearch 기반 PoC)</p>
        <!-- 챗봇 메시지 영역 -->
        <div class="chat-container mb-4 p-2 bg-white rounded-lg border border-gray-200">
            <div v-for="msg in chatMessages" :key="msg.id" :class="{'text-right': msg.sender === 'user'}" class="mt-3">
                <span :class="{'bg-green-200 text-green-800': msg.sender === 'ai', 'bg-indigo-200 text-indigo-800': msg.sender === 'user'}"
                      class="inline-block p-3 rounded-lg chat-bubble shadow-md">
                    {{ msg.content }}
                </span>
            </div>
            <div ref="chatEnd"></div>
        </div>
        <!-- 챗봇 입력 -->
        <div class="flex">
            <input type="text" placeholder="질문 입력"
                   class="flex-grow p-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
                   v-model="userQuery" @keyup.enter="$emit('submit-chat', userQuery)">
            <button @click="$emit('submit-chat', userQuery)" :disabled="isChatting"
                    class="bg-green-600 text-white px-6 py-3 rounded-r-lg hover:bg-green-700 transition disabled:opacity-50">
                {{ isChatting ? '처리 중...' : '질문하기' }}
            </button>
        </div>
    </div>
</div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    selectedArticle: Object,
    relatedArticles: Array,
    getMainTopic: Function,
    currentUser: Object,
    chatMessages: Array,
    isChatting: Boolean
});

const emit = defineEmits(['go-to-main', 'select-article', 'toggle-like', 'submit-chat']);
const userQuery = ref(''); // 입력 상태는 이 컴포넌트에서 관리
</script>