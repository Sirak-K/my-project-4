

# URLS - APP (CORE)

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('new_post/', views.new_post, name='new_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/', views.group_details, name='group_details'),
    path('private_messages/', views.private_messages, name='private_messages'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
