from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import Article, UserLike, UserReadHistory
from .serializers import ArticleSerializer, UserLikeSerializer, UserReadHistorySerializer

# 1. 기사 관련 모든 동작 (조회, 상세 보기, 좋아요)
class ArticleViewSet(viewsets.ModelViewSet):
    # 최신 기사 순서대로 가져오기
    queryset = Article.objects.all().order_by('-published_at')
    serializer_class = ArticleSerializer
    
    # 누구나 기사 목록은 볼 수 있음
    permission_classes = [AllowAny] 

    # [특수 기능] 특정 기사에 '좋아요' 누르기 (POST /api/v1/articles/{id}/like/)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        article = self.get_object() # 현재 기사 가져오기
        user = request.user         # 요청한 사용자 가져오기
        
        # 이미 좋아요를 눌렀다면? -> 좋아요 취소 (Toggle 방식)
        if UserLike.objects.filter(user=user, article=article).exists():
            UserLike.objects.filter(user=user, article=article).delete()
            return Response({'message': '좋아요 취소'}, status=status.HTTP_200_OK)
        
        # 안 눌렀다면? -> 좋아요 생성
        UserLike.objects.create(user=user, article=article)
        return Response({'message': '좋아요 완료!'}, status=status.HTTP_201_CREATED)

# 2. 읽은 기록 관련 동작 (내 기록 보기)
class UserReadHistoryViewSet(viewsets.ModelViewSet):
    queryset = UserReadHistory.objects.all()
    serializer_class = UserReadHistorySerializer
    permission_classes = [IsAuthenticated] # 로그인한 사람만 가능

    # '전체 기록'이 아니라 '내가 읽은 기록'만 가져오도록 필터링
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)