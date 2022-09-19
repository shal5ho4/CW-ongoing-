from django.contrib import admin
from .models import Tweets

@admin.register(Tweets)
class TweetsAdmin(admin.ModelAdmin):
  list_display = ['user', 'created_at', 'will_post', 'is_active']
  list_filter = ['created_at']