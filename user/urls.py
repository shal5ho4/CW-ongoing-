from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
  #path('login/', views.user_login, name='login'),
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('dashboard/<slug:slug>/', views.tweet_detail, name='detail'),
  path('tweet_create/', views.tweet_create_form, name='create'),
  path('', views.top_page, name='top'),
]