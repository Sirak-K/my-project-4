# "CB" = CODEBASE

# --------- CB 1 - ADMIN ---------
from django.contrib import admin
from .models import Comment, Like, Post, Profile, FriendList, FriendRequest

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(FriendList)
admin.site.register(FriendRequest)


# --------- CB 2 - MODELS ---------
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

# MODEL 1 - PROFILE
class Profile(models.Model):
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True) 
    bio = models.TextField(blank=True, null=True)

    PROFESSION_CHOICES = (
        ('O', 'Student'),
        ('M', 'Working'),
        ('F', 'Not Working'),
        ('T', 'Other'),
        ('N', 'None selected'),
    )
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES, default="N", blank=True, null=True)

    GENDER_CHOICES = (
        ('O', 'Other'),
        ('M', 'He/Him'),
        ('F', 'She/Her'),
        ('T', 'They/Them'),
        ('N', 'None selected'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
# DECOR 2 - PROFILE: CREATE
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# MODEL 3 - POST
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key relationship with User
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the post is created
    def time_since_posted(self):
        now = timezone.now()
        time_difference = now - self.created_at
        if time_difference.seconds < 60:
            return "Just now"
        return f"{timesince(self.created_at)} ago"

    def count_likes(self):
        return self.likes.count()

    def count_comments(self):
        return self.comments.count()
    
    def __str__(self):
        return f"{self.author.username}'s Post"
# MODEL 4 - COMMENT
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author.username}'s comment on {self.post}"
# MODEL 5 - LIKE
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} liked {self.post.author.username}'s Post"
# MODEL 6 - FRIEND REQUEST
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    status = models.CharField(max_length=20)  # "Pending", "Accepted", "Rejected"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} sent a friend request to {self.recipient.username}"
# MODEL 7 - FRIEND LIST
class FriendList(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_lists_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_lists_user2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username} are friends"


# --------- CB 3 - URLS 1 ---------
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
    # path('post_comment/<int:post_id>/post_comment', views.post_comment, name='post_comment'), 
    path('post_create/', views.post_create, name='post_create'),
    path('post_details/<int:post_id>/', views.post_details, name='post_details'),  
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


# --------- CB 4 - VIEWS ---------

import json
import traceback  # Add this import

from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, UpdateProfileForm, UpdateProfileImageForm
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import Comment, Post, Profile, FriendList, FriendRequest

# VIEW 1 - HOME 
def index(request):
    if request.user.is_authenticated:
        post_list = Post.objects.all().order_by('-created_at')
        paginator = Paginator(post_list, 10)  # Show 10 posts per page

        page = request.GET.get('page')
        posts = paginator.get_page(page)

        friends_sent = FriendRequest.objects.filter(sender=request.user, status='accepted')
        friends_received = FriendRequest.objects.filter(recipient=request.user, status='accepted')
        friends = [fr.from_user for fr in friends_received] + [fr.to_user for fr in friends_sent]

        latest_posts = Post.objects.filter(author__in=friends).order_by('-created_at')[:10]

        context = {
            'posts': posts,
            'latest_posts': latest_posts
        }
        return render(request, 'user_feed.html', context)
    else:
        return render(request, 'login.html')
# VIEW 2 - SIGNUP
def signup_view(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        # Create a user creation form with the POST data
        form = UserCreationForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the user to the database
            user = form.save()
            # Log the user in
            login(request, user)
            # Redirect the user to the user_feed page
            return redirect('user_feed')  # Change this line
    else:
        # If it's not a POST request, create an empty form
        form = UserCreationForm()
    # Render the signup template with the form
    return render(request, 'signup.html', {'form': form})
# ---------> VIEW 3 - [ LOG-IN ] --------->
def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_feed')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_feed')
            else:
                return render(request, 'login.html', {'error': 'Invalid login credentials'})
        else:
            logout(request) 
            return render(request, 'login.html')
# VIEW 4 - LOGGED-IN - USER FEED
@login_required
def user_feed(request):
    # Fetching friend relationships
    friends = friendships(request.user)

    # Fetching posts from friends and the current user
    posts = Post.objects.filter(author__in=friends + [request.user]).order_by('-created_at')
    
    # Adding pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
    }
    return render(request, 'user_feed.html', context)
# VIEW 5 - LOGGED-IN - PROFILE
@csrf_exempt
@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    friends = friend_list(request)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile', user_id=user.id)
    else:
        form = UpdateProfileForm(instance=user_profile)

    context = {'user_profile': user_profile, 'user_posts': user_posts, 'friends': friends, 'form': form}
    return render(request, 'user_profile.html', context)
# VIEW 6 - LOGGED-IN - PROFILE - UPLOAD IMAGES
@login_required
def user_profile_image(request, user_id):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UpdateProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile image and banner updated successfully.')
            return redirect('user_profile', user_id=user.id)
    else:
        form = UpdateProfileImageForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'user_profile_image.html', context)
# VIEW 7 - LOGGED-IN - PROFILE - UPDATE PROFILE DETAILS
@require_POST
@csrf_exempt
@login_required
def user_profile_field_update(request, user_id):
    try:
        data = json.loads(request.body)
        print(f"Received data: {data}")

        field_name = data.get('fieldName')
        field_value = data.get('value')
        if field_name in ['bio', 'gender', 'profession']:
            user_profile = Profile.objects.get(user__id=user_id)
            setattr(user_profile, field_name, field_value)
            user_profile.save()
            return JsonResponse({"status": "success"})
        else:
            return HttpResponseBadRequest("Invalid field")
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        return JsonResponse({"status": "error", "message": str(e)})
# ---------> VIEW 8 - [ LOG-OUT ] --------->
def logout_view(request):
    logout(request)
    return redirect('login_view')
# VIEW 9 - POST: CREATE
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})
# VIEW 10 - POST: COMMENTS
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_details', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'post_comment.html', {'form': form, 'post': post})
# VIEW 11 - POST: LIKES
@require_POST
def post_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({"likes": post.likes})
    else:
        return HttpResponseNotAllowed(['POST'])
# VIEW 12 - POST: DETAILS
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'post_details.html', {'post': post, 'comments': comments})
# VIEW 13 - POST: REMOVE
@login_required
def post_remove(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('user_feed')

    context = {'post': post}
    return render(request, 'post_remove.html', context)
# VIEW 14 - POST: LIST
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'post_list.html', {'posts': posts})
# --------- VIEW 15 - FRIEND REQUEST ---------
@login_required
def friend_request(request):
    pending_friend_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')
    
    return render(request, 'friend_request.html', {'pending_friend_requests': pending_friend_requests})
# VIEW 16 - FRIENDSHIPS
def friendships(user):
    friends_sent = FriendRequest.objects.filter(sender=user, status='accepted')
    friends_received = FriendRequest.objects.filter(recipient=user, status='accepted')
    friends = [fr.recipient for fr in friends_sent] + [fr.sender for fr in friends_received]
    return friends
# VIEW 17 - FRIEND REQUEST: ACCEPT
@login_required
def friend_request_accept(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.recipient != request.user:
        messages.error(request, "You cannot accept this friend request.")
        return redirect('friend_list')

    friend_request.status = 'accepted'
    friend_request.save()

    messages.success(request, f"You are now friends with {friend_request.sender.username}.")
    return redirect('friend_list')
# VIEW 18 - FRIEND REQUEST: REJECT
@login_required
def friend_request_reject(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.recipient != request.user:
        messages.error(request, "You cannot reject this friend request.")
        return redirect('friend_list')

    friend_request.status = 'rejected'
    friend_request.save()

    messages.success(request, f"You have rejected the friend request from {friend_request.sender.username}.")
    return redirect('friend_list')
# VIEW 19 - FRIEND LIST 
@login_required
def friend_list(request):
    # Fetching friend relationships
    friends_sent = FriendRequest.objects.filter(sender=request.user, status='accepted')
    friends_received = FriendRequest.objects.filter(recipient=request.user, status='accepted')
    friends = [fr.recipient for fr in friends_sent] + [fr.sender for fr in friends_received]

    # Fetching pending friend requests sent by the user
    pending_sent = FriendRequest.objects.filter(sender=request.user, status='pending')

    # Fetching pending friend requests received by the user
    pending_received = FriendRequest.objects.filter(recipient=request.user, status='pending')

    context = {
        'friends': friends,
        'pending_sent': pending_sent,
        'pending_received': pending_received,
    }
    return render(request, 'friend_list.html', context)

# --------- CB 5 - FORMS ---------
from django import forms
from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'privacy_settings']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'gender', 'profession', ]
class UpdateProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'banner_image' ]


# --------- CB 6 - SIGNALS ---------
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
User = get_user_model()
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(id_user=instance.username, user=instance)


# --------- CB 7 - APPS --------- 
from django.apps import AppConfig
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
def ready(self):
        import core.signals


# --------- CB 8 - URLS 2 ---------
# URLS - PROJECT (SOCIALIZE)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)


# --------- CB 9 - HTML/JS FILES ---------
# ALL THE HTML TEMPLATES USED IN THE SOCIAL NETWORKING PROJECT

# 1: base.html
# 2: error_page.html
# 3: footer.html
# 4: forgot_password
# 5: friend_list.html
# 6: header_logged_in.html
# 7: header_not_logged_in.html
# 8: index.html
# 9: login.html
# 10: logout.html
# 11: post_comment.html
# 12: post_create.html
# 13: post_details.html
# 14: post_list.html
# 15: post_remove.html
# 16: signup.html
# 17: user_feed.html
# 18: user_profile.image.html
# 19: user_profile.html

# JAVASCRIPT-FILES USED 
# 1: script.js