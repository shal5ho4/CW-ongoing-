from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Tweets(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='tweets_created',
    on_delete=models.CASCADE
  )
  tweet = models.CharField(max_length=180)
  slug = models.SlugField(max_length=200, blank=True, unique=True)
  created_at = models.DateField(auto_now_add=True)
  will_post = models.DateField(blank=True)
  is_active = models.BooleanField(default=False)

  def __str__(self):
    return self.created_at
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.created_at)
    super().save(*args, **kwargs)