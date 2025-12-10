from django.contrib import admin
from .models import Article, Interaction, DailyReport

admin.site.register(Article)
admin.site.register(Interaction)
admin.site.register(DailyReport)