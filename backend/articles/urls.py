from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, UserReadHistoryViewSet

# 라우터가 자동으로 URL 생성
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)       # /articles/ 로 접속하면 기사 목록
router.register(r'history', UserReadHistoryViewSet) # /history/ 로 접속하면 읽은 기록

urlpatterns = [
    path('', include(router.urls)),
]