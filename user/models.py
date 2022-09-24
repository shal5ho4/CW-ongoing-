from django.db import models
from django.conf import settings
from django.utils import timezone
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
  

  def save(self, *args, **kwargs):
    if not self.slug:
      id = str(self.user.id)
      usr = UserSocialAuth.objects.get(user_id=self.user.id)
      data = usr.access_token
      screen_name = data['screen_name']
      slug = f'{screen_name}_{id}'
      self.slug = slug
    super().save(*args, **kwargs)

  def __str__(self):
    return self.slug
  