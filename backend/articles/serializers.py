from rest_framework import serializers
from .models import Article, Interaction

# 1. 기사(Article) 변환기
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'  # 모든 필드(제목, 내용, 카테고리 등)를 JSON으로 변환

# 2. 좋아요(UserLike), 읽은 기록(UserReadHistory) 변환기
class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'
        read_only_fields = ('user',) # 유저는 자동으로 들어가게