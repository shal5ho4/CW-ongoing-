from django import forms
from django.utils import timezone
from django.utils.text import slugify
from .models import Tweets
from datetime import timedelta

HOURS = [
  (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
  (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11),
  (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17),
  (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)
]


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


class TweetCreateForm(forms.ModelForm):
  
  def clean(self):
    cd = super().clean()
    will_post = cd.get('will_post')
    will_post_time = cd.get('will_post_time')

    will_post_after = will_post + timedelta(hours=will_post_time)
    today = timezone.now()

    if will_post_after < today:
      raise forms.ValidationError('')
    
    return cd

  def save(self, force_insert=False, force_update=False, commit=True):
    tweet = super().save(commit=False)
    slug = slugify(tweet.publish)
    tweet.slug = slug
    
    will_post = tweet.will_post
    will_post_time = tweet.will_post_time
    new_will_post = will_post + timedelta(hours=will_post_time)
    tweet.will_post = new_will_post

    if commit:
      tweet.save()
      
    return tweet
  
  class Meta:
    model = Tweets
    fields = ('will_post', 'will_post_time', 'tweet')
    widgets = {
      'will_post': forms.SelectDateWidget,
      'will_post_time': forms.widgets.Select(choices=HOURS),
      'tweet': forms.Textarea(
        attrs={
          'class': 'form-cotrol shadow px-2',
          'rows': 6
        }
      )
    }
