import random
import time
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from articles.models import Article, Interaction
from faker import Faker # pip install faker 필요

User = get_user_model()

class Command(BaseCommand):
    help = '사용자 및 활동(좋아요/읽음) 더미 데이터 생성'

    def handle(self, *args, **options):
        fake = Faker('ko_KR')
        
        # 1. 더미 유저 생성 (10명)
        self.stdout.write('더미 유저 생성 중...')
        users = []
        for _ in range(10):
            username = fake.user_name()
            # 중복 방지
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='password123', # 테스트용 비번 통일
                    email=fake.email()
                )
                users.append(user)
        
        # 기존 유저도 포함
        users.extend(list(User.objects.all()))
        
        articles = list(Article.objects.all())
        if not articles:
            self.stdout.write(self.style.ERROR('기사가 없습니다. 먼저 RSS 수집을 진행하세요.'))
            return

        self.stdout.write(self.style.SUCCESS(f'총 {len(users)}명의 유저와 {len(articles)}개의 기사로 활동 로그를 생성합니다.'))

        # 2. 활동 로그 생성 (무한루프 아님, 100개만 생성)
        # (무한으로 돌리고 싶으면 range(100) 대신 while True 사용)
        count = 0
        for _ in range(100): 
            user = random.choice(users)
            article = random.choice(articles)
            action = random.choice(['LIKE', 'READ'])

            # 중복 체크 (이미 좋아요/읽음 한 경우 패스하거나 갱신)
            if not Interaction.objects.filter(user=user, article=article, type=action).exists():
                Interaction.objects.create(
                    user=user,
                    article=article,
                    type=action
                )
                count += 1
                if count % 10 == 0:
                    self.stdout.write(f'... {count}개 생성 완료')

        self.stdout.write(self.style.SUCCESS(f'총 {count}개의 더미 Interaction 데이터 생성 완료!'))
