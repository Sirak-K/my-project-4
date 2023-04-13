# URLS - APP (CORE)

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    # URLS #1 - FRIENDS
    path('friend_list/', views.friend_list, name='friend_list'),
    path('friend_request/', views.friend_request, name='friend_request'),
    path('friend_request_accept/<int:request_id>/', views.friend_request_accept, name='friend_request_accept'),
    path('friend_request_reject/<int:request_id>/', views.friend_request_reject, name='friend_request_reject'),
    # URLS - LOG-IN / LOG-OUT
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
  # URLS - POSTS
    path('post_comment/<int:post_id>/', views.post_comment, name='post_comment'), 
    path('post_create/', views.post_create, name='post_create'),
    path('post_details/<int:post_id>/', views.post_details, name='post_details'),  
    path('post_edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('post_like/<int:post_id>/', views.post_like, name='post_like'),
    path('post_remove/<int:post_id>/', views.post_remove, name='post_remove'),
    # URLS - PROFILE
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    # URLS - SIGNUP
    path('signup/', views.signup_view, name='signup_view'),
    # URLS - USER_PROFILE
    path('user_profile/<int:user_id>/update_field/', views.user_profile_field_update, name='user_profile_field_update'),
    path('user_profile_image/<int:user_id>/', views.user_profile_image, name='user_profile_image'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_feed', views.user_feed, name='user_feed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)