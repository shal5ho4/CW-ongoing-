from django import forms
from .models import Tweets


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


class TweetCreateForm(forms.ModelForm):
  class Meta:
    model = Tweets
    fields = ('will_post', 'tweet')
    widgets = {
      'will_post': forms.SelectDateWidget,
      'tweet': forms.Textarea(attrs={'rows': 6})
    }
