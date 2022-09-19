from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from .forms import LoginForm

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

  user = UserSocialAuth.objects.get(user_id=request.user.id)
  
  return render(request, 'user/dashboard.html', 
    {'section': 'dashboard', 'user': user}
  )
