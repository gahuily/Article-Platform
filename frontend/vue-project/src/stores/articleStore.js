import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

export const useArticleStore = defineStore('article', () => {
    const articlesData = ref([]);
    const readArticles = ref([]);

    const getMainTopic = (article) => {
        const topicMap = {
            'IT': ['AI', '반도체', 'HBM', '클라우드', '개발자'],
            '금융': ['금융', '증시', '금리', '투자'],
            '환경': ['환경', '기후', '식량', '농업'],
            '스포츠': ['축구', '스포츠', '리그', '유럽'],
        };
        if (!article || !article.keywords) return '기타';
        for (const mainTopic in topicMap) {
            if (article.keywords.some((k) => topicMap[mainTopic].some((rk) => k.includes(rk)))) {
                return mainTopic;
            }
        }
        return '기타';
    };

    const fetchArticles = async () => {
        console.log('API: 기사 데이터 로드 요청 (미구현)');
    };

    const latestArticles = computed(() => {
        return articlesData.value.slice().sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
    });

    const topTopics = computed(() => {
        const counts = {};
        readArticles.value.forEach((r) => {
            const t = getMainTopic(r);
            if (t && t !== '기타') counts[t] = (counts[t] || 0) + 1;
        });
        return Object.entries(counts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 3)
            .map(([keyword, count]) => ({ keyword, count }));
    });

    return {
        articlesData,
        readArticles,
        latestArticles,
        topTopics,
        fetchArticles,
        getMainTopic,
    };
});