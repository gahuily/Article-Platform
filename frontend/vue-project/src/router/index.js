import { createRouter, createWebHistory } from 'vue-router';

// 1. 필요한 페이지 컴포넌트들을 import 합니다.
import LoginPage from '../pages/LoginPage.vue';
import RegisterPage from '../pages/RegisterPage.vue';
import MainPage from '../pages/MainPage.vue';
import ArticleDetail from '../pages/ArticleDetail.vue';
import Dashboard from '../pages/Dashboard.vue';
import MyPage from '../pages/MyPage.vue'; 

const router = createRouter({
  // URL 히스토리 모드 설정 (웹 앱 표준)
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: LoginPage },
    { path: '/register', name: 'register', component: RegisterPage },
    { path: '/', name: 'main', component: MainPage },
    { path: '/article/:id', name: 'detail', component: ArticleDetail },
    { path: '/dashboard', name: 'dashboard', component: Dashboard },
    { path: '/mypage', name: 'mypage', component: MyPage },
  ],
});

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user_token');

  if (authRequired && !loggedIn) {
    return next('/login');
  }
  next();
});

export default router;