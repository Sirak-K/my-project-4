# URLS - APP (CORE)

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('new_post/', views.new_post, name='new_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('friend_list/', views.friend_list, name='friend_list'),
    path('friend_request/', views.friend_request, name='friend_request'),
    path('notifications/', views.notifications, name='notifications'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/', views.group_details, name='group_details'),
    path('private_messages/', views.private_messages, name='private_messages'),
    path('signup/', views.signup_view, name='signup_view'),

    path('page_logged_out', views.logged_out_view, name='logged_out_view'),
    path('logged_in/', views.logged_in_view, name='logged_in_view'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
