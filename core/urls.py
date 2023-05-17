# File: urls.py - APP (CORE)

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import  PostDeleteView, PostCreateView, PostListView, PostDetailsView



urlpatterns = [
    
    path('', views.user_feed, name='home'),

  
    path('signup/', views.signup_view, name='signup'),
    # URLS - LOG-IN / LOG-OUT
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    # URLS - USER
    path('user_feed/', views.user_feed, name='user_feed'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile_image/', views.user_profile_image, name='user_profile_image'),
    path('user_profile_field_update/<int:user_id>/', views.user_profile_field_update, name='user_profile_field_update'),


    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/', PostDetailsView.as_view(), name='post_details'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('posts/', PostListView.as_view(), name='post_list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)