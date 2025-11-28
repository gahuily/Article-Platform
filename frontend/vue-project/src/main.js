import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; 

// 🚨 Pinia 파일의 경로를 명확히 지정: './stores/index.js'
// (Pinia를 초기화하는 코드가 이 파일에 들어있어야 합니다.)
import pinia from './stores/index.js'; 

const app = createApp(App);

app.use(pinia);
app.use(router);

app.mount('#app');