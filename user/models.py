from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class Tweets(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='tweets_created',
    on_delete=models.CASCADE
  )
  tweet = models.CharField(max_length=50)
  slug = models.SlugField(unique_for_date='publish')
  publish = models.DateTimeField(default=timezone.now)
  created_at = models.DateTimeField(auto_now_add=True)
  will_post = models.DateTimeField()
  will_post_time = models.IntegerField(default=0)
  is_posted = models.BooleanField(default=False)
  task_id = models.CharField(max_length=255, blank=True)
  
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name_plural = 'Tweets'

  def __str__(self):
    return self.slug

  def get_absolute_url(self):
    return reverse('detail', args=[self.slug])

  def get_seconds(self):
    dt1 = self.created_at
    dt2 = self.will_post
    
    td = dt2 - dt1
    td_sec = int(td.total_seconds())

    return td_sec

  