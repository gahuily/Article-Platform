from django.db import models
from django.conf import settings

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('IT', 'IT/테크'),
        ('ECONOMY', '경제/금융'), 
        ('SOCIETY', '환경/사회'),
        ('SPORTS', '스포츠'), 
        ('LIFE', '생활'), 
        ('CULTURE', '문화/예술'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    source = models.CharField(max_length=50)
    original_url = models.URLField()
    image_url = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    keywords = models.TextField(blank=True, help_text="기사 키워드 (쉼표 구분)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class UserLike(models.Model):
    """사용자가 기사에 '좋아요'를 누른 기록"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='liked_by')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
        ordering = ['-liked_at']

    def __str__(self):
        return f"{self.user} liked {self.article.title}"

class UserReadHistory(models.Model):
    """사용자가 기사를 읽은 기록"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='read_history')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='read_by')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
        ordering = ['-read_at']

    def __str__(self):
        return f"{self.user} read {self.article.title}"

class DailyReport(models.Model):
    """배치 파이프라인(Airflow)의 결과 리포트"""
    report_date = models.DateField(unique=True)
    total_articles_collected = models.IntegerField(help_text="HDFS 로그 기반 배치 분석 결과")
    top_keyword_1 = models.CharField(max_length=100, blank=True, help_text="가장 많이 언급된 키워드 (HDFS 기반)")
    top_keyword_2 = models.CharField(max_length=100, blank=True)
    top_keyword_3 = models.CharField(max_length=100, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-report_date']

    def __str__(self):
        return f"Report for {self.report_date}"