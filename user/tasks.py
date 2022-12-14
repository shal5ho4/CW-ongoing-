from celery import task
from django.conf import settings
from social_django.models import UserSocialAuth
from .models import Tweets
from datetime import timedelta
import tweepy
import sched
import time
  

@task
def schedule(tweet_id):

  def tweet_create():
    tweet = Tweets.objects.get(id=tweet_id)
    user1 = tweet.user
    user2 = UserSocialAuth.objects.get(user_id=user1.id)
    
    text = tweet.tweet
    url = tweet.get_absolute_url()
    seconds = tweet.get_seconds()
    days = timedelta(seconds=seconds).days
    
    if days == 0:
      hr = int(seconds / 3600)

      if hr == 0:
        min = int(seconds / 60)
        status = f'私は{min}分前に「{text}」と予言しました。 \n' \
                 f'https://mysite.com:8000{url}'
      else:
        status = f'私は{hr}時間前に「{text}」と予言しました。 \n' \
                 f'https://mysite.com:8000{url}'
    else:
      status = f'私は{days}日前に「{text}」と予言しました。 \n' \
               f'https://mysite.com:8000{url}'
    
    tokens = user2.access_token
    ck = settings.SOCIAL_AUTH_TWITTER_KEY
    cs = settings.SOCIAL_AUTH_TWITTER_SECRET
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])

    api = tweepy.API(auth)
    api.update_status(status=status)

    tweet.is_posted = True
    tweet.save()
  
  def getseconds(tweet_id):
    tweet = Tweets.objects.get(id=tweet_id)
    return tweet.get_seconds()

  td_sec = getseconds(tweet_id)
  s = sched.scheduler(time.time, time.sleep)
  s.enter(td_sec, 1, tweet_create)
  s.run()
