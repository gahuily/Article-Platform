<template>
<div class="space-y-6">
    
    <!-- 검색 서비스 (Elasticsearch 연동) -->
    <div class="card-bg p-6 rounded-xl shadow-md">
        <div class="flex space-x-3">
            <input type="text" placeholder="실시간 뉴스 검색 (Elasticsearch 기반)"
                   class="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800">
            <button class="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition font-semibold">
                검색
            </button>
        </div>
    </div>
    
    <!-- A. 맞춤 추천 섹션 -->
    <div class="card-bg p-6 rounded-xl shadow-md border-l-4 border-indigo-500">
        <h2 class="text-2xl font-bold text-indigo-700 mb-4 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.085 15.545a2.5 2.5 0 01-3.642 0L6 14.18V8.75a3 3 0 013-3h6a3 3 0 013 3v5.43l-1.443 1.365a2.5 2.5 0 01-3.642 0z"/></svg>
            {{currentUser.username}}님 맞춤 추천 (규칙 기반 큐레이션)
        </h2>
        <p class="text-sm text-gray-600 mb-4">
            관심 키워드 ('{{currentUser.keywords}}') 매칭 결과를 우선적으로 보여드립니다.
        </p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div v-for="article in recommendedArticles" :key="article.id"
                 @click="$emit('select-article', article)"
                 class="bg-gray-50 p-4 rounded-lg hover:ring-2 hover:ring-indigo-400 cursor-pointer transition shadow-sm">
                <p class="text-xs text-indigo-500 mb-1 font-semibold">#{{ getMainTopic(article) }}</p>
                <h3 class="font-semibold text-gray-800 line-clamp-2">{{ article.title }}</h3>
                <p class="text-xs text-gray-500 mt-1">{{ article.summary }}</p>
            </div>
        </div>
    </div>
    
    <!-- B. 뉴스 피드 및 카테고리 탭 -->
    <div class="space-y-4 pt-4">
        
        <h2 class="text-2xl font-bold text-gray-800">전체 최신 뉴스 피드</h2>
        
        <!-- 토픽 필터 탭 -->
        <div class="flex space-x-4 border-b border-gray-200 bg-white p-3 rounded-xl shadow-sm">
            <button @click="$emit('update:currentTopic', '전체')" :class="{'active-tab': currentTopic === '전체'}" class="px-4 py-2 text-gray-600 hover:text-indigo-600 transition">전체</button>
            <button @click="$emit('update:currentTopic', 'IT')" :class="{'active-tab': currentTopic === 'IT'}" class="px-4 py-2 text-gray-600 hover:text-indigo-600 transition">IT/테크</button>
            <button @click="$emit('update:currentTopic', '금융')" :class="{'active-tab': currentTopic === '금융'}" class="px-4 py-2 text-gray-600 hover:text-indigo-600 transition">경제/금융</button>
            <button @click="$emit('update:currentTopic', '환경')" :class="{'active-tab': currentTopic === '환경'}" class="px-4 py-2 text-gray-600 hover:text-indigo-600 transition">환경/사회</button>
            <button @click="$emit('update:currentTopic', '스포츠')" :class="{'active-tab': currentTopic === '스포츠'}" class="px-4 py-2 text-gray-600 hover:text-indigo-600 transition">스포츠</button>
        </div>

        
        <div class="space-y-4">
            <div v-for="article in filteredArticles" :key="article.id"
                 class="bg-white p-6 rounded-xl shadow-sm flex justify-between items-start hover:ring-2 hover:ring-indigo-200 transition">
                <div @click="$emit('select-article', article)" class="cursor-pointer flex-grow">
                    <p class="text-sm text-gray-500 mb-1">
                        <span class="inline-block bg-indigo-50 text-indigo-600 text-xs px-2 py-1 rounded-full mr-2 font-semibold">
                            {{ getMainTopic(article) }}
                        </span>
                        | {{ article.published_at }} | 출처: {{ article.source }}
                    </p>
                    <h3 class="text-xl font-bold text-gray-900 mb-2">{{ article.title }}</h3>
                    <p class="text-base text-gray-600">{{ article.summary }}</p>
                </div>
                <button @click.stop="$emit('toggle-like', article)"
                        :class="{'text-red-500': article.isLiked, 'text-gray-400': !article.isLiked}"
                        class="p-2 ml-4 rounded-full hover:bg-red-50 transition">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">좋아요</span>
                </button>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    currentUser: Object,
    recommendedArticles: Array,
    filteredArticles: Array,
    getMainTopic: Function,
    currentTopic: String // V-model 처리를 위해 prop으로 받음
});

const emit = defineEmits(['select-article', 'toggle-like', 'update:currentTopic']);
</script>