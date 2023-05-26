# File: urls.py - APP (CORE)

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import UserProfileImageView, UserProfileFieldUpdateView, PostLikeToggleView, UserFeedView, LogoutView, LoginView, SignUpView, UserSearchView, UserProfileView, FriendAcceptView, FriendRejectView, FriendCancelView, FriendListView, FriendRequestView, CommentCreateView, PostDeleteView, PostCreateView, PostListView, PostDetailsView



urlpatterns = [

    # URLS - SIGN-UP
    path('signup/', SignUpView.as_view(), name='signup'),
    # URLS - LOG-IN / LOG-OUT
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # URLS - USER
    path('user_feed/', UserFeedView.as_view(), name='user_feed'),
    path('', UserFeedView.as_view(), name='user_feed'),


    
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('user_profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
   
    path('user_profile_image/', UserProfileImageView.as_view(), name='user_profile_image'),
    path('user_profile_image/<str:username>/', UserProfileImageView.as_view(), name='user_profile_image'),
    
    path('user_profile_field_update/<int:user_id>/', UserProfileFieldUpdateView.as_view(), name='user_profile_field_update'),


  
    path('user_search/', UserSearchView.as_view(), name='user_search'),
    
    




    # URLS - Friendship
    path('friend_list/', FriendListView.as_view(), name='friend_list'),
    path('friend_request/', FriendRequestView.as_view(), name='friend_request'),
    path('friend_request/add/<int:pk>/', FriendRequestView.as_view(), name='friend_add'),
    path('friend_request/accept/<int:pk>/', FriendAcceptView.as_view(), name='friend_accept'),
    path('friend_request/reject/<int:pk>/', FriendRejectView.as_view(), name='friend_reject'),
    path('friend_request/cancel/<int:pk>/', FriendCancelView.as_view(), name='friend_cancel'),

   


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