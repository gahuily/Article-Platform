from rest_framework import serializers
from .models import Article, UserLike, UserReadHistory

# 1. 기사(Article) 변환기
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'  # 모든 필드(제목, 내용, 카테고리 등)를 JSON으로 변환

# 2. 좋아요(UserLike) 변환기
class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLike
        fields = '__all__'

# 3. 읽은 기록(UserReadHistory) 변환기
class UserReadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReadHistory
        fields = '__all__'