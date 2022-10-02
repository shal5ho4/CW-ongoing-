from django.contrib import admin
from .models import Tweets

@admin.register(Tweets)
class TweetsAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'publish', 'will_post', 'is_posted']
  list_filter = ['created_at', 'will_post']
  list_editable = ['is_posted']