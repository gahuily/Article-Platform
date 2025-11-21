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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('LIKE', '좋아요'),
        ('READ', '읽음 (클릭)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interactions')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='interactions')
    
    type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']