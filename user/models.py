from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from social_django.models import UserSocialAuth
import datetime


class Tweets(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='tweets_created',
    on_delete=models.CASCADE
  )
  tweet = models.CharField(max_length=50)
  slug = models.SlugField(max_length=50, blank=True, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  will_post = models.DateTimeField(validators=[MinValueValidator(timezone.now)])
  will_post_time = models.IntegerField(default=0)
  is_posted = models.BooleanField(default=False)
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name_plural = 'Tweets'
  

  def get_seconds(self):
    dt1 = self.created_at
    dt2 = self.will_post + datetime.timedelta(hours=self.will_post_time)
    td = dt2 - dt1
    td_sec = int(td.total_seconds())
    
    return td_sec

  def __str__(self):
    return self.slug
  