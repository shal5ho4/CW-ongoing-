from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social_django.models import UserSocialAuth
from PJ.celery import app as celery_app
from .forms import TweetCreateForm
from .models import Tweets
from .tasks import schedule


def top_page(request):
  if request.user.is_authenticated:
    return redirect('create')

  return render(request, 'user/top.html')


@login_required
def dashboard(request):
  posted = Tweets.objects.filter(user=request.user, is_posted=True)
  scheduled = Tweets.objects.filter(user=request.user, is_posted=False)
  user = UserSocialAuth.objects.get(user_id=request.user.id)

  paginator = Paginator(posted, 10)
  page = request.GET.get('page')

  try:
    posted = paginator.page(page)
  except PageNotAnInteger:
    posted = paginator.page(1)
  except EmptyPage:
    posted = paginator.page(paginator.num_pages)

  return render(request, 'user/dashboard.html', 
    {'posted': posted, 'scheduled': scheduled, 'user': user, 'page': page})


@login_required
def tweet_detail(request, slug):
  tweet = get_object_or_404(Tweets, slug=slug)
  
  if request.method == 'POST':
    edit_form = TweetCreateForm(request.POST, instance=tweet)

    if request.POST.get('next', '') == 'delete':
      celery_app.control.revoke(tweet.task_id, terminate=True, signal='SIGKILL')
      tweet.delete()
      messages.success(request, 'ツイートを削除しました。')

      return redirect('dashboard')
    
    elif request.POST.get('next', '') == 'update' \
         and edit_form.is_valid():
      
      edit_form.save()
      celery_app.control.revoke(tweet.task_id, terminate=True, signal='SIGKILL')
      schedule.delay(tweet.id)
      messages.success(request, 'ツイート内容を更新しました。')

      return redirect('dashboard')
    
    else:
      messages.error(request, 'ツイートは50文字以内で入力してください。')
  
  else:
    edit_form = TweetCreateForm(instance=tweet)

  return render(request, 'user/tweet_detail.html', 
    {'tweet': tweet, 'edit_form': edit_form}
  )


@login_required
def tweet_create_form(request):
  if request.user.is_superuser:
    return redirect('admin/login/')

  if request.method == 'POST':
    form = TweetCreateForm(request.POST)
    
    if form.is_valid():
      new_tweet = form.save(commit=False)
      new_tweet.user = request.user
      new_tweet.save()

      task = schedule.delay(new_tweet.id)
      new_tweet.task_id = task.id
      new_tweet.save()
      
      messages.success(request, 'ツイートを登録しました。')
      
      return redirect('dashboard')
    
    else:
      messages.error(
        request, '日付は本日以降で、ツイートは50文字以内で入力してください。'
      )

  else:
    form = TweetCreateForm()

  return render(request, 'user/tweet_create.html', {'form': form})
