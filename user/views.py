from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from social_django.models import UserSocialAuth
from .forms import TweetCreateForm
from .models import Tweets
from .tasks import schedule


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
def tweet_detail(request, slug):
  tweet = get_object_or_404(Tweets, slug=slug)
  
  return render(request, 'user/tweet_detail.html', {'tweet': tweet})


@login_required
def tweet_create_form(request):
  if request.method == 'POST':
    form = TweetCreateForm(request.POST)
    
    if form.is_valid():
      cd = form.cleaned_data
      new_tweet = form.save(commit=False)
      new_tweet.user = request.user
      new_tweet.save()

      schedule.delay(new_tweet.id)
      messages.success(request, 'ツイートを登録しました。')

      return redirect('dashboard')
    
    else:
      messages.error(request, '日付は本日以降で、ツイートは50文字以内で入力してください。')
  
  else:
    form = TweetCreateForm()
  
  return render(request, 'user/tweet_create.html', {'form': form})