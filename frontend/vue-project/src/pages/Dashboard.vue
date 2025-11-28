<template>
<div class="space-y-8">
    <h2 class="text-3xl font-bold text-gray-800 mb-4">📊 사용자 활동 및 통계 대시보드</h2>
    <p class="text-sm text-gray-500 border-b pb-4">
        * 활동 기록(좋아요, 읽음) 및 배치 파이프라인(Airflow/Cron)의 리포트 결과를 시각화합니다.
    </p>

    <!-- 1. 핵심 성과 지표 (KPIs) -->
    <div class="grid md:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-xl shadow-md border-l-4 border-purple-500">
            <p class="text-sm font-medium text-purple-600">나의 총 좋아요 수</p>
            <p class="text-3xl font-bold text-purple-900 mt-1">{{ likedArticlesList.length }}개</p>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-md border-l-4 border-green-500">
            <p class="text-sm font-medium text-green-600">가장 관심있게 읽은 뉴스</p>
            <p v-if="mostReadArticle" class="text-lg font-bold text-green-900 mt-1 line-clamp-2" :title="mostReadArticle.title">
                {{ mostReadArticle.title }}
            </p>
            <p v-else class="text-lg font-bold text-green-900 mt-1">N/A</p>
        </div>
    </div>
    
    <!-- 2. 활동 시각화: 주간 읽은 기사 수 -->
    <div class="bg-white p-6 rounded-xl shadow-md">
        <h3 class="text-xl font-semibold mb-4 text-gray-800">🗓️ 주간 읽은 기사 수 (활동 시각화)</h3>
        <div class="h-64 flex justify-around items-end p-4 border-b border-l border-gray-300">
            <!-- Chart.js 그래프 대용 -->
            <div v-for="(count, day) in readHistory" :key="day" class="flex flex-col items-center w-1/7">
                <div :style="{height: (count) + 'px', minHeight: '5px'}" class="w-8 bg-indigo-500 rounded-t-lg transition-all duration-300 hover:bg-indigo-600 cursor-pointer" :title="`${day}: ${count}건`"></div>
                <span class="text-xs mt-1 text-gray-600">{{ day }}</span>
            </div>
        </div>
    </div>
    
    <!-- 3. 많이 읽은 분야 TOP 3 -->
    <div class="bg-white p-6 rounded-xl shadow-md">
        <h3 class="text-xl font-semibold mb-4 text-gray-800">🔥 많이 읽은 분야 TOP 3 ({{ topTopics.length }}개 분석됨)</h3>
        <div class="space-y-3">
            <div v-for="(topic, index) in topTopics" :key="topic.keyword" 
                 class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span class="text-lg font-bold w-10 text-center text-indigo-600">{{ index + 1 }}위</span>
                <span class="text-lg font-semibold flex-grow text-gray-700">{{ topic.keyword }} 분야</span>
                <span class="text-sm text-gray-500">{{ topic.count }}회 조회</span>
            </div>
            <p v-if="topTopics.length === 0" class="text-gray-500 text-center py-4">아직 읽은 기사가 충분하지 않아 토픽을 분석할 수 없습니다.</p>
        </div>
    </div>

    <!-- 4. 좋아요/읽은 기사 목록 (최신 5건) -->
    <div class="grid md:grid-cols-2 gap-6">
        <!-- 좋아요한 기사 목록 -->
        <div class="bg-white p-6 rounded-xl shadow-md">
            <h3 class="text-xl font-semibold mb-4 text-gray-800">❤️ 좋아요한 기사 ({{ likedArticlesList.length }}건)</h3>
            <ul class="space-y-3">
                <li v-for="article in likedArticlesList" :key="article.id"
                    class="border-b border-gray-100 pb-2 last:border-b-0 cursor-pointer hover:text-indigo-600"
                    @click="$emit('select-article-by-id', article.id)">
                    <p class="font-medium text-gray-700 truncate">{{ article.title }}</p>
                    <p class="text-xs text-gray-500">{{ article.published_at }} | {{ article.source }}</p>
                </li>
                <li v-if="likedArticlesList.length === 0" class="text-gray-500">좋아요한 기사가 없습니다.</li>
            </ul>
        </div>

        <!-- 최근 읽은 기사 목록 -->
        <div class="bg-white p-6 rounded-xl shadow-md">
            <h3 class="text-xl font-semibold mb-4 text-gray-800">📚 최근 읽은 기록 (최신 5건)</h3>
            <ul class="space-y-3">
                <li v-for="read in readArticles.slice(0, 5)" :key="read.read_at + read.id"
                    class="border-b border-gray-100 pb-2 last:border-b-0 cursor-pointer hover:text-indigo-600"
                    @click="$emit('select-article-by-id', read.id)">
                    <p class="font-medium text-gray-700 truncate">{{ read.title }}</p>
                    <p class="text-xs text-gray-500">읽은 시간: {{ read.read_at }}</p>
                </li>
                <li v-if="readArticles.length === 0" class="text-gray-500">읽은 기록이 없습니다.</li>
            </ul>
        </div>
    </div>
</div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    likedArticlesList: Array,
    topTopics: Array,
    mostReadArticle: Object,
    readHistory: Object,
    readArticles: Array
});

const emit = defineEmits(['select-article-by-id']);
</script>