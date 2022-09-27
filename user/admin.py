from django.contrib import admin
from .models import Tweets

@admin.register(Tweets)
class TweetsAdmin(admin.ModelAdmin):
  list_display = ['user', 'publish', 'will_post', 'is_posted']
  list_filter = ['created_at']