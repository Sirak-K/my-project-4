from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    PostCreateView, PostListView, PostDetailsView,
    UserProfileView, CommentCreateView, PostDeleteView, 
    PasswordResetView, UserDeletionView, FriendshipManager,
    UserFeedView, LogoutView, LoginView, SignUpView, UserSearchView,
    UserProfileImageView, UserProfileFieldUpdateView, PostLikeToggleView,PostEditView
)

urlpatterns = [

    # URLS - SIGN-UP, LOG-IN, LOG-OUT
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),

    # URLS - PASSWORD RESET 
    path('password_reset_page/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/success/', PasswordResetView.as_view(), name='password_reset_success'),

    # URLS - USER
    path('', UserFeedView.as_view(), name='user_feed'),
    path('user_feed/', UserFeedView.as_view(), name='user_feed'),
    path('user_search/', UserSearchView.as_view(), name='user_search'),
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('user_profile/<str:username>/', UserProfileView.as_view(), name='user_profile'), 
    path('user_profile_image/', UserProfileImageView.as_view(), name='user_profile_image'),
    path('user_deletion_confirmation/', UserDeletionView.as_view(), name='user_deletion_confirmation'),
    path('user_profile_image/<str:username>/', UserProfileImageView.as_view(), name='user_profile_image'),
    path('user_profile_field_update/<int:user_id>/', UserProfileFieldUpdateView.as_view(), name='user_profile_field_update'),

    # URLS - FRIENDSHIP
    path('friend_list/', FriendshipManager.as_view(), name='friend_list'),
    path('friend_request/', FriendshipManager.as_view(), name='friend_request'),
    path('existing_friends/', FriendshipManager.as_view(), name='existing_friends'),
    path('friendship/remove/<int:friendship_id>/', FriendshipManager.as_view(), name='remove_friendship'),
    path('friend_request/send/<int:receiver_id>/', FriendshipManager.as_view(), name='send_friend_request'),
    path('friend_request/cancel/<int:request_id>/', FriendshipManager.as_view(), name='cancel_friend_request'),
    path('friend_request/accept/<int:request_id>/', FriendshipManager.as_view(), name='accept_friend_request'),
    path('friend_request/reject/<int:request_id>/', FriendshipManager.as_view(), name='reject_friend_request'),

    # URLS - POST & POST COMMENTS
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_details/', PostDetailsView.as_view(), name='post_details'),
    path('post_details/<int:pk>/', PostDetailsView.as_view(), name='post_details'),
    path('post_details/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    
    path('post_edit_page/<int:pk>/', PostEditView.as_view(), name='post_edit_page'),
    path('post_edit_page/<int:pk>/save_edit', PostEditView.as_view(), name='post_edit_save'),


    path('post_details/toggle-like/<int:pk>/', PostLikeToggleView.as_view(), name='toggle_like'),
    path('post_comment/<int:pk>/comment/create/', CommentCreateView.as_view(), name='post_comment_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)