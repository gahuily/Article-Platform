import feedparser
from dateutil import parser
from django.core.management.base import BaseCommand
from articles.models import Article
from datetime import datetime
import time

class Command(BaseCommand):
    help = '주요 언론사 RSS 데이터 수집'

    def handle(self, *args, **options):
        # 1. 수집할 RSS 목록 정의 (제공해주신 리스트 반영)
        rss_list = [
            # 경향신문
            ('경향신문', 'POLITICS', 'https://www.khan.co.kr/rss/rssdata/politic_news.xml'),
            ('경향신문', 'ECONOMY', 'https://www.khan.co.kr/rss/rssdata/economy_news.xml'),
            ('경향신문', 'SOCIETY', 'https://www.khan.co.kr/rss/rssdata/society_news.xml'),
            ('경향신문', 'INTERNATIONAL', 'https://www.khan.co.kr/rss/rssdata/kh_world.xml'),
            ('경향신문', 'SPORTS', 'http://www.khan.co.kr/rss/rssdata/kh_sports.xml'),
            ('경향신문', 'CULTURE', 'https://www.khan.co.kr/rss/rssdata/culture_news.xml'),
            ('경향신문', 'ENTERTAINMENT', 'https://www.khan.co.kr/rss/rssdata/kh_entertainment.xml'),

            # 서울신문
            ('서울신문', 'POLITICS', 'https://www.seoul.co.kr/xml/rss/rss_politics.xml'),
            ('서울신문', 'SOCIETY', 'https://www.seoul.co.kr/xml/rss/rss_society.xml'),
            ('서울신문', 'ECONOMY', 'https://www.seoul.co.kr/xml/rss/rss_economy.xml'),
            ('서울신문', 'INTERNATIONAL', 'https://www.seoul.co.kr/xml/rss/rss_international.xml'),
            ('서울신문', 'CULTURE', 'https://www.seoul.co.kr/xml/rss/rss_life.xml'), # 문화/건강 -> LIFE로 매핑
            ('서울신문', 'SPORTS', 'https://www.seoul.co.kr/xml/rss/rss_sports.xml'),
            ('서울신문', 'ENTERTAINMENT', 'https://www.seoul.co.kr/xml/rss/rss_entertainment.xml'),

            # SBS
            ('SBS', 'POLITICS', 'https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=01&plink=RSSREADER'),
            ('SBS', 'SOCIETY', 'https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=03&plink=RSSREADER'),
            ('SBS', 'ECONOMY', 'https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=02&plink=RSSREADER'),
            ('SBS', 'INTERNATIONAL', 'https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=07&plink=RSSREADER'),
            ('SBS', 'CULTURE', 'https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=08&plink=RSSREADER'), # 생활/문화 -> CULTURE
            ('SBS', 'ENTERTAINMENT', 'https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=14&plink=RSSREADER'),
            ('SBS', 'SPORTS', 'https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=09&plink=RSSREADER'),
        ]

        total_count = 0

        self.stdout.write(self.style.WARNING('RSS 수집을 시작합니다...'))

        for source_name, category, url in rss_list:
            try:
                feed = feedparser.parse(url)
                self.stdout.write(f'[{source_name}-{category}] 파싱 중... ({len(feed.entries)}개)')

                for entry in feed.entries:
                    # 2. 중복 체크 (이미 저장된 링크면 건너뜀)
                    if Article.objects.filter(original_url=entry.link).exists():
                        continue

                    # 3. 날짜 파싱 (RSS마다 날짜 포맷이 다를 수 있어 dateutil 사용)
                    published_at = datetime.now()
                    if hasattr(entry, 'published'):
                        try:
                            published_at = parser.parse(entry.published)
                        except:
                            pass
                    
                    # 4. 이미지 추출 (RSS는 이미지가 없을 수도, enclosure에 있을 수도 있음)
                    image_url = None
                    if 'enclosures' in entry and len(entry.enclosures) > 0:
                        image_url = entry.enclosures[0].get('href')
                    elif 'media_content' in entry and len(entry.media_content) > 0:
                        image_url = entry.media_content[0].get('url')

                    # 5. DB 저장
                    Article.objects.create(
                        title=entry.title,
                        content=entry.description, # 요약본 저장
                        summary=entry.description[:100] + '...', # 짧게 잘라서 저장
                        category=category,
                        source=source_name,
                        original_url=entry.link,
                        image_url=image_url,
                        published_at=published_at
                    )
                    total_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error parsing {url}: {e}'))
                continue
            
            # 서버 부하 방지를 위해 잠깐 대기
            time.sleep(0.5)

        self.stdout.write(self.style.SUCCESS(f'총 {total_count}개의 새로운 기사를 수집했습니다!'))