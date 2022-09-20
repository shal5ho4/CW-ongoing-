from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from .forms import LoginForm, TweetCreateForm
import tweepy


# not for production
def user_login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)

    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(request, 
        username=cd['username'], password=cd['password'])
      
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponse('Authenticated successfully')

        else:
          return HttpResponse('Disabled account')
      
      else:
        return HttpResponse('Invalid login')

  else:
    form = LoginForm()
  return render(request, 'user/login.html', {'form': form})


@login_required
def dashboard(request):
  if request.user.is_superuser:
    return redirect('/admin/login/')

  user1 = User.objects.get(id=request.user.id)
  user2 = UserSocialAuth.objects.get(user_id=request.user.id)

  if request.method == 'POST':
    form = TweetCreateForm(request.POST)
    
    if form.is_valid():
      cd = form.cleaned_data
      new_tweet = form.save(commit=False)
      tweet = new_tweet.tweet
      new_tweet.user = user1
      new_tweet.save()

      userdata = user2.access_token
      ck = settings.SOCIAL_AUTH_TWITTER_KEY
      cs = settings.SOCIAL_AUTH_TWITTER_SECRET

      auth = tweepy.OAuthHandler(ck, cs)
      auth.set_access_token(userdata['oauth_token'], userdata['oauth_token_secret'])

      api = tweepy.API(auth)
      api.update_status(status=tweet)

      return redirect('dashboard')

  else:
    form = TweetCreateForm()
  return render(request, 'user/dashboard.html', 
    {'section': 'dashboard', 'user': user2, 'form': form}
  )
