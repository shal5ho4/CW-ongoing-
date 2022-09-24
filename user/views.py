from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from social_django.models import UserSocialAuth
from .forms import TweetCreateForm
from .models import Tweets
import tweepy


def top_page(request):
  if request.user.is_authenticated:
    return redirect('create')

  return render(request, 'user/top.html')


@login_required
def dashboard(request):
  if request.user.is_superuser:
    return redirect('admin/login/')
  
  tweets = Tweets.objects.filter(user=request.user)
  user = UserSocialAuth.objects.get(user_id=request.user.id)

  return render(request, 'user/dashboard.html', {'tweets': tweets, 'user': user})


@login_required
def tweet_create(request):
  user1 = User.objects.get(id=request.user.id)
  user2 = UserSocialAuth.objects.get(user_id=user1.id)
  
  if request.method == 'POST':
    form = TweetCreateForm(request.POST)
    
    if form.is_valid():
      cd = form.cleaned_data
      new_tweet = form.save(commit=False)
      new_tweet.user = user1
      text = new_tweet.tweet
      new_tweet.save()

      tokens = user2.access_token
      ck = settings.SOCIAL_AUTH_TWITTER_KEY
      cs = settings.SOCIAL_AUTH_TWITTER_SECRET

      auth = tweepy.OAuthHandler(ck, cs)
      auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])

      api = tweepy.API(auth)
      api.update_status(status=text)

      messages.success(request, 'ツイートを登録しました。')

      return redirect('dashboard')
    
    else:
      messages.error(request, '日付は本日以降で、ツイートは50文字以内で入力してください。')
  
  else:
    form = TweetCreateForm()
  
  return render(request, 'user/tweet_create.html', {'form': form})