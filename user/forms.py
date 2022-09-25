from django import forms
from django.utils.text import slugify
from .models import Tweets

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

  def save(self, force_insert=False, force_update=False, commit=True):
    tweet = super().save(commit=False)
    slug = slugify(tweet.will_post) # ここかえる
    tweet.slug = slug

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
