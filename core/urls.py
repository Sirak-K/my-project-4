# File: urls.py - APP (CORE)

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import   UserDeletionView, FriendshipManager, UserProfileImageView, UserProfileFieldUpdateView, PostLikeToggleView, UserFeedView, LogoutView, LoginView, SignUpView, UserSearchView, UserProfileDetailsView, UserProfileView, CommentCreateView, PostDeleteView, PostCreateView, PostListView, PostDetailsView



urlpatterns = [

    # URLS - SIGN-UP
    path('signup/', SignUpView.as_view(), name='signup'),
   
   
    # URLS - LOG-IN / LOG-OUT
    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),


    path('user_deletion_confirmation/', UserDeletionView.as_view(), name='user_deletion_confirmation'),

    # URLS - USER
    path('user_feed/', UserFeedView.as_view(), name='user_feed'),
    path('', UserFeedView.as_view(), name='user_feed'),




    path('user_profile_field_update/<int:user_id>/', UserProfileFieldUpdateView.as_view(), name='user_profile_field_update'),
  
    path('user_search/', UserSearchView.as_view(), name='user_search'),
    
    
    # URLS - User Profile View
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('user_profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
   
    path('user_profile_image/', UserProfileImageView.as_view(), name='user_profile_image'),
    path('user_profile_image/<str:username>/', UserProfileImageView.as_view(), name='user_profile_image'),



    
    

# URLS - Existing Friendships
path('existing_friends/', FriendshipManager.as_view(), name='existing_friends'),

# URLS - Friend List view
path('friend_list/', FriendshipManager.as_view(), name='friend_list'),
# URLS - Friend Request view
path('friend_request/', FriendshipManager.as_view(), name='friend_request'),


path('friendship/remove/<int:friendship_id>/', FriendshipManager.as_view(), name='remove_friendship'),



path('friend_request/send/<int:receiver_id>/', FriendshipManager.as_view(), name='send_friend_request'),

path('friend_request/cancel/<int:request_id>/', FriendshipManager.as_view(), name='cancel_friend_request'),
path('friend_request/accept/<int:request_id>/', FriendshipManager.as_view(), name='accept_friend_request'),
path('friend_request/reject/<int:request_id>/', FriendshipManager.as_view(), name='reject_friend_request'),






    # URLS - POST
    path('post_details/toggle-like/<int:pk>/', PostLikeToggleView.as_view(), name='toggle_like'),
    path('post_details/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post_details_page/<int:pk>/', PostDetailsView.as_view(), name='post_details_page'),
    path('post_details', PostDetailsView.as_view(), name='post_details'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('posts/', PostListView.as_view(), name='post_list'),
    # URLS - POST COMMENTS
    path('post/<int:pk>/comment/create/', CommentCreateView.as_view(), name='post_comment_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)