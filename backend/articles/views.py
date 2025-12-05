from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

# 1. models.py에 정의된 이름인 Interaction을 가져옵니다.
from .models import Article, Interaction

from .serializers import ArticleSerializer, InteractionSerializer

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
        article = self.get_object()
        user = request.user
        
        # Interaction 모델에서 type='LIKE'인 데이터를 찾습니다.
        filtered_like = Interaction.objects.filter(
            user=user, 
            article=article, 
            type='LIKE'
        )

        if filtered_like.exists():
            # 이미 있으면 삭제 (좋아요 취소)
            filtered_like.delete()
            return Response({'message': '좋아요 취소'}, status=status.HTTP_200_OK)
        
        # 없으면 생성 (좋아요)
        Interaction.objects.create(
            user=user, 
            article=article, 
            type='LIKE'
        )
        return Response({'message': '좋아요 완료!'}, status=status.HTTP_201_CREATED)

# 2. 읽은 기록 관련 동작 (내 기록 보기)
class UserReadHistoryViewSet(viewsets.ModelViewSet):
    # Interaction 모델을 기반으로 동작합니다.
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer # 시리얼라이저도 Interaction용으로 변경 필요
    permission_classes = [IsAuthenticated] # 로그인한 사람만 가능

    def get_queryset(self):
        # 1) 현재 접속한 유저의 데이터이면서
        # 2) type이 'READ' (읽음) 인 데이터만 가져오기
        return self.queryset.filter(user=self.request.user, type='READ')
