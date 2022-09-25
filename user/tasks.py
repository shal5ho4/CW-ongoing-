from celery import task
from django.conf import settings
from social_django.models import UserSocialAuth
from .models import Tweets
import tweepy
import sched
import time


# @task
# def tweet_create(tweet_id):
#   new_tweet = Tweets.objects.get(id=tweet_id)
#   user1 = new_tweet.user
#   user2 = UserSocialAuth.objects.get(user_id=user1.id)
  
#   text = new_tweet.tweet
#   tokens = user2.access_token

#   ck = settings.SOCIAL_AUTH_TWITTER_KEY
#   cs = settings.SOCIAL_AUTH_TWITTER_SECRET
#   auth = tweepy.OAuthHandler(ck, cs)
#   auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])

#   api = tweepy.API(auth)
#   api.update_status(status=text)
  

@task
def schedule(tweet_id):
  global tweet
  tweet = Tweets.objects.get(id=tweet_id)

  def tweet_create():
    user1 = tweet.user
    user2 = UserSocialAuth.objects.get(user_id=user1.id)
    
    text = tweet.tweet
    tokens = user2.access_token

    ck = settings.SOCIAL_AUTH_TWITTER_KEY
    cs = settings.SOCIAL_AUTH_TWITTER_SECRET
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])

    api = tweepy.API(auth)
    api.update_status(status=text)

  td_sec = 10 # ここかえる

  s = sched.scheduler(time.time, time.sleep)
  s.enter(td_sec, 1, tweet_create)
  s.run()
