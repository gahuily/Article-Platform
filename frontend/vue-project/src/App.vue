<template>
<div id="app" class="p-4 sm:p-6">
    
    <header v-if="$route.path !== '/login' && $route.path !== '/register'" class="card-bg p-4 rounded-xl card-shadow mb-6">
        <div class="flex justify-between items-center">
            <h1 @click="$router.push({name: 'main'})" class="text-2xl font-bold text-indigo-700 cursor-pointer">
                R/T News <span class="text-gray-500">큐레이션</span>
            </h1>
            
            <nav class="flex space-x-6 items-center">
                <button @click="$router.push({name: 'main'})" :class="{'text-indigo-600 font-bold': $route.name === 'main', 'text-gray-600 hover:text-indigo-600': $route.name !== 'main'}"
                        class="transition">
                    뉴스 피드
                </button>
                <button @click="$router.push({name: 'dashboard'})" :class="{'text-indigo-600 font-bold': $route.name === 'dashboard', 'text-gray-600 hover:text-indigo-600': $route.name !== 'dashboard'}"
                        class="transition">
                    활동 대시보드
                </button>
                <button @click="$router.push({name: 'mypage'})" :class="{'text-indigo-600 font-bold': $route.name === 'mypage', 'text-gray-600 hover:text-indigo-600': $route.name !== 'mypage'}"
                        class="transition">
                    마이페이지
                </button>
                
                <span class="text-gray-700 font-semibold">{{ currentUser.username || '게스트' }}님</span>
                <button @click="handleLogout" class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition font-semibold">
                    로그아웃
                </button>
            </nav>
        </div>
    </header>

    <main>
        <router-view v-slot="{ Component }">
            <component :is="Component"
                       v-bind="{
                           currentUser,
                           recommendedArticles,
                           filteredArticles,
                           getMainTopic,
                           currentTopic,
                           latestArticles,
                           selectArticle,
                           toggleLike,
                           likedArticlesList,
                           topTopics,
                           mostReadArticle,
                           readHistory,
                           readArticles
                       }"
                       @select-article-by-id="selectArticleById"
            />
        </router-view>
    </main>
</div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from './stores/user';

// ********************************************
// 6개 페이지 컴포넌트 Import (1-1에서 생성한 파일들)
// ********************************************
import LoginPage from './pages/LoginPage.vue';
import RegisterPage from './pages/RegisterPage.vue';
import MainPage from './pages/MainPage.vue';
import ArticleDetail from './pages/ArticleDetail.vue';
import Dashboard from './pages/Dashboard.vue';
import MyPage from './pages/MyPage.vue';
// ********************************************

// --- (2) 상태 관리 (State) ---
const view = ref('login'); // 현재 뷰 상태 (라우팅 역할)
const mypageTab = ref('topics'); 
const selectedArticle = ref(null);
const currentTopic = ref('전체'); // 메인 페이지 필터 상태

// 회원가입 관련 상태
const availableTopics = ['IT/테크', '경제/금융', '환경/사회', '스포츠', '생활', '문화/예술'];
const regSelectedTopics = ref([]); // 회원가입 시 선택된 토픽

// 상세 페이지 챗봇 상태
const userQuery = ref('');
const isChatting = ref(false);
const chatMessages = ref([
    { id: 1, sender: 'ai', content: '안녕하세요 UserA님. 이 기사에 대해 궁금한 점이 있으신가요?' }
]);
const chatEnd = ref(null); 

// Pinia user store (development simulation)
const userStore = useUserStore();
const currentUser = userStore.user;
// Safe accessor: if store.user is temporarily undefined, provide a fallback shape
const currentUserSafe = computed(() => {
    try {
        return (currentUser && currentUser.value) ? currentUser.value : { id: null, username: '', keywords: '', likedArticles: [] };
    } catch (e) {
        return { id: null, username: '', keywords: '', likedArticles: [] };
    }
});
const router = useRouter();

// 기사 데이터 (나중에 API로 대체될 부분)
const articlesData = ref([
    {
        id: 1,
        title: 'AI 반도체 시장, 2026년 3배 성장 전망',
        summary: 'HBM 수요 폭증에 따른 국내 기업들의 공격적인 투자 계획 발표...',
        content: 'AI 반도체 시장이 고성능 컴퓨팅 및 클라우드 서비스의 성장세에 힘입어 2026년까지 현재 규모의 3배 이상으로 성장할 것으로 예상됩니다. 삼성전자와 SK하이닉스는 고대역폭 메모리(HBM) 생산량을 대폭 늘려 시장 점유율을 확대할 계획입니다.',
        published_at: '2025.11.21',
        source: '데일리 IT',
        keywords: ['AI', '반도체', 'HBM', '투자'],
        likes: 15,
        link: '#',
        isLiked: false,
    },
    {
        id: 2,
        title: '글로벌 증시, 예상치 상회하는 실적에 소폭 상승',
        summary: '미국 중앙은행의 금리 동결 시사 이후 투자 심리가 회복...',
        content: '글로벌 주요 증시가 기업들의 3분기 실적 발표에 힘입어 긍정적인 흐름을 보였습니다. 특히 기술주 중심의 나스닥은 1% 이상 상승하며 활기를 띠었고, 전문가들은 연말 랠리에 대한 기대를 높이고 있습니다.',
        published_at: '2025.11.20',
        source: '월드 경제신문',
        keywords: ['금융', '증시', '투자', '금리'],
        likes: 22,
        link: '#',
        isLiked: true,
    },
    {
        id: 3,
        title: '기후 변화로 인한 식량 불안정 심화, 국제적 대응 촉구',
        summary: '이상 기후가 농작물 수확량에 미치는 영향 분석 보고서...',
        content: '최근 발표된 보고서에 따르면, 전 세계적으로 빈번해지는 이상 기후 현상이 주요 농작물의 수확량을 감소시키고 있어 식량 안보에 대한 위협이 커지고 있습니다.',
        published_at: '2025.11.20',
        source: '녹색 환경 네트워크',
        keywords: ['환경', '기후', '식량', '농업'],
        likes: 8,
        link: '#',
        isLiked: false,
    },
    {
        id: 4,
        title: '유럽 축구 리그 이변 속출, 약팀들의 반란',
        summary: '주요 리그에서 예상 밖의 결과가 나오며 순위 경쟁이 치열...',
        content: '이번 주말 유럽 주요 축구 리그에서 하위권 팀들이 상위권 팀들을 연이어 격파하는 이변이 발생했습니다.',
        published_at: '2025.11.19',
        source: '스포투데이',
        keywords: ['축구', '스포츠', '리그', '유럽'],
        likes: 30,
        link: '#',
        isLiked: true,
    },
    {
        id: 5,
        title: '대형 IT 기업, 개발자 인력 충원 가속화',
        summary: '인공지능 및 클라우드 분야 인력난 해소를 위한 공격적인 채용 전략...',
        content: '글로벌 IT 대기업들이 AI 엔지니어와 클라우드 솔루션 개발자 등 전문 인력 확보를 위해 경쟁적으로 채용 규모를 늘리고 있습니다.',
        published_at: '2025.11.18',
        source: '테크 브리핑',
        keywords: ['IT', '개발자', '클라우드', 'AI'],
        likes: 10,
        link: '#',
        isLiked: false,
    },
]);

// 사용자 활동 데이터 (나중에 API로 대체될 부분)
const readArticles = ref([
    { id: 1, title: articlesData.value.find(a => a.id === 1).title, keywords: articlesData.value.find(a => a.id === 1).keywords, read_at: '2025.11.21 14:30' },
    { id: 5, title: articlesData.value.find(a => a.id === 5).title, keywords: articlesData.value.find(a => a.id === 5).keywords, read_at: '2025.11.21 14:35' }, 
    { id: 3, title: articlesData.value.find(a => a.id === 3).title, keywords: articlesData.value.find(a => a.id === 3).keywords, read_at: '2025.11.21 10:15' },
    { id: 4, title: articlesData.value.find(a => a.id === 4).title, keywords: articlesData.value.find(a => a.id === 4).keywords, read_at: '2025.11.20 18:00' },
    { id: 1, title: articlesData.value.find(a => a.id === 1).title, keywords: articlesData.value.find(a => a.id === 1).keywords, read_at: '2025.11.20 09:00' },
    { id: 3, title: articlesData.value.find(a => a.id === 3).title, keywords: articlesData.value.find(a => a.id === 3).keywords, read_at: '2025.11.19 16:45' },
]);
const readHistory = ref({
    Mon: 80, Tue: 120, Wed: 100, Thu: 150, Fri: 180, Sat: 90, Sun: 60 // 주간 읽은 기사 수 시뮬레이션 데이터
});

// --- (3) 계산된 속성 (Computed Properties) ---

const latestArticles = computed(() => {
    const liked = (currentUserSafe.value && Array.isArray(currentUserSafe.value.likedArticles)) ? currentUserSafe.value.likedArticles : [];
    articlesData.value.forEach(article => {
        article.isLiked = liked.includes(article.id);
    });
    return articlesData.value.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
});

const likedArticlesList = computed(() => {
    return latestArticles.value.filter(article => article.isLiked);
});

const topTopics = computed(() => {
    const keywordCounts = {};
    readArticles.value.forEach(read => {
        let mainTopic = getMainTopic(read);
        if (mainTopic && mainTopic !== '기타') {
            keywordCounts[mainTopic] = (keywordCounts[mainTopic] || 0) + 1;
        }
    });

    return Object.entries(keywordCounts)
        .sort(([, countA], [, countB]) => countB - countA)
        .slice(0, 3)
        .map(([keyword, count]) => ({ keyword, count }));
});

const mostReadArticle = computed(() => {
    const articleCounts = {};
    readArticles.value.forEach(read => {
        articleCounts[read.id] = (articleCounts[read.id] || 0) + 1;
    });

    const sortedArticles = Object.entries(articleCounts).sort(([, countA], [, countB]) => countB - countA);
    if (sortedArticles.length === 0) return null;
    
    const mostReadId = sortedArticles[0][0];
    return articlesData.value.find(a => a.id == mostReadId) || null;
});

const recommendedArticles = computed(() => {
    const kw = (currentUserSafe.value && currentUserSafe.value.keywords) ? currentUserSafe.value.keywords : '';
    const userKeywords = kw.split(',').map(k => k.trim().toLowerCase()).filter(Boolean);
    if (userKeywords.length === 0) return latestArticles.value.slice(0, 4);
    return latestArticles.value.filter(article => {
        return article.keywords.some(k => userKeywords.includes(k.toLowerCase()));
    }).slice(0, 4);
});

const filteredArticles = computed(() => {
    if (currentTopic.value === '전체') {
        return latestArticles.value;
    }
    return latestArticles.value.filter(article => 
        getMainTopic(article) === currentTopic.value
    );
});

const relatedArticles = computed(() => {
    if (!selectedArticle.value) return [];
    const currentTopic = getMainTopic(selectedArticle.value);
    
    return articlesData.value
        .filter(article => article.id !== selectedArticle.value.id)
        .filter(article => getMainTopic(article) === currentTopic)
        .slice(0, 2);
});


// --- (4) 함수 (Methods/Actions) ---

const getMainTopic = (article) => {
    const topicMap = {
        'IT': ['AI', '반도체', 'HBM', '클라우드', '개발자'],
        '금융': ['금융', '증시', '금리', '투자'],
        '환경': ['환경', '기후', '식량', '농업'],
        '스포츠': ['축구', '스포츠', '리그', '유럽']
    };
    for (const mainTopic in topicMap) {
        if (article.keywords.some(k => topicMap[mainTopic].some(rk => k.includes(rk)))) {
            return mainTopic;
        }
    }
    return '기타';
};

const selectArticle = (article) => {
    console.log(`[Django API 연동 필요]: 기사 ID ${article.id}에 대한 읽은 기록 저장 및 Kafka 발행`);
    
    article.content = "이것은 기사의 전체 본문입니다. Flink에서 정제된 데이터가 PostgreSQL에 저장되었으며, Django API를 통해 조회되었습니다. 사용자가 기사를 클릭했으므로, 이 시점에 '읽은 기록'이 Django 백엔드를 통해 PostgreSQL에 저장되고 Kafka의 user_activity_topic에 발행됩니다.";
    selectedArticle.value = article;

    if (view.value !== 'detail') {
        const uname = (userStore.user && userStore.user.value && userStore.user.value.username) ? userStore.user.value.username : '게스트';
        chatMessages.value = [{ id: 1, sender: 'ai', content: `안녕하세요 ${uname}님. 이 기사(${article.title.substring(0, 10)}...)에 대해 궁금한 점이 있으신가요?` }];
    }
    view.value = 'detail';
};

const selectArticleById = (id) => {
    const article = articlesData.value.find(a => a.id === id);
    if (article) {
        selectArticle(article);
    }
};

const toggleLike = (article) => {
    article.isLiked = !article.isLiked;
    if (article.isLiked) {
        article.likes++;
        // write through to the store (ensure array exists)
        if (!userStore.user.value.likedArticles) userStore.user.value.likedArticles = [];
        userStore.user.value.likedArticles.push(article.id);
    } else {
        article.likes--;
        const arr = userStore.user.value.likedArticles || [];
        const index = arr.indexOf(article.id);
        if (index !== -1) {
            arr.splice(index, 1);
        }
        userStore.user.value.likedArticles = arr;
    }
    console.log(`[Django/Kafka 연동 필요]: 좋아요 상태 변경 이벤트 발생. PostgreSQL 'user_likes' 테이블 업데이트 및 Kafka 'user_activity_topic'에 발행.`);
};

const submitChat = (query) => { // 챗봇 메시지 전송 로직
    if (!query.trim()) return;

    // (로직 생략 - App.vue 외부에서 호출 시 인자를 받아야 함)
    // 실제 App.vue에서는 이 로직이 구현되어 있습니다.
    console.log(`[챗봇 시뮬레이션]: 질문 '${query}'에 대해 Elasticsearch 검색 및 응답 생성 요청.`);
};

const updateTopics = (updatedTopics) => { // 마이페이지 관심 분야 업데이트
    // write to store
    userStore.user.value.keywords = updatedTopics.join(', ');
    console.log(`[Django API 연동 시뮬레이션]: 관심 분야 업데이트: ${userStore.user.value.keywords}`);
    alert("관심 분야 설정이 성공적으로 업데이트되었습니다! (시뮬레이션)");
};

const deleteSingleLike = (articleId) => { // 좋아요 개별 삭제
    const confirmed = window.confirm("선택한 좋아요 기록을 삭제하시겠습니까?");
    if (confirmed) {
        const arr = userStore.user.value.likedArticles || [];
        const index = arr.indexOf(articleId);
        if (index !== -1) {
            arr.splice(index, 1);
        }
        userStore.user.value.likedArticles = arr;
        const article = articlesData.value.find(a => a.id === articleId);
        if (article && article.isLiked) {
            article.isLiked = false;
            article.likes--;
        }
        console.log(`[Django API 연동 시뮬레이션]: PostgreSQL user_likes 테이블에서 ArticleID: ${articleId}의 기록 삭제 요청`);
    }
};

const deleteSingleRead = (index) => { // 읽은 기록 개별 삭제
    const confirmed = window.confirm("선택한 읽은 기록을 삭제하시겠습니까?");
    if (confirmed) {
        readArticles.value.splice(index, 1);
        console.log(`[Django API 연동 시뮬레이션]: PostgreSQL user_read_history 테이블에서 기록 삭제 요청`);
        alert(`읽은 기록이 삭제되었습니다! (시뮬레이션)`);
    }
};

const handleLogout = () => {
    userStore.logout();
    router.push({ name: 'login' });
};

</script>