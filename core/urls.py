from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('new_post/', views.new_post, name='new_post'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/', views.group_details, name='group_details'),
    path('private_messages/', views.private_messages, name='private_messages'),
]
