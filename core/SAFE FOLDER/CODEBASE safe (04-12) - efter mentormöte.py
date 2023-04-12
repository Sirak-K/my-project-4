# "CB" = CODEBASE

# --------- CB 1 - ADMIN ---------

from django.contrib import admin
from .models import GroupPost, Comment, Like, Post, Profile, FriendList, FriendRequest, Notification, Group, GroupMember, Message

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FriendList)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupPost)


# --------- CB 2 - MODELS ---------
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save

# MODEL 1 - PROFILE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # One-to-one relationship with User
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    privacy_settings = models.CharField(max_length=30, blank=True, null=True)
    # website = models.URLField(blank=True)
    # phone_number = models.CharField(max_length=20, blank=True)
    # gender = models.CharField(choices=GENDER_CHOICES, max_length=2, blank=True)
    
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
    privacy_settings = models.CharField(max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the post is created
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
# MODEL 8 - NOTIFICATION
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)  # "friend_request", "like", "comment", etc.
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Set to False by default
    def __str__(self):
        return f"{self.user.username}'s {self.type} Notification"
# MODEL 9 - PRIVATE MESSAGES 
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender.username} sent a message to {self.recipient.username}"
# MODEL 10 - GROUP
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} Group"
# MODEL 11 - GROUP MEMBERS
class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} is a member of {self.group.name}"
# MODEL 12 - GROUP POSTS
class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='group_posts/', blank=True, null=True)
    video = models.FileField(upload_to='group_videos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author.username}'s Post in {self.group.name} Group"
    

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
    path('friend_list/', views.friend_list, name='friend_list'),
    path('friend_request/', views.friend_request, name='friend_request'),
    path('friend_request_accept/<int:request_id>/', views.friend_request_accept, name='friend_request_accept'),
    path('friend_request_reject/<int:request_id>/', views.friend_request_reject, name='friend_request_reject'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/', views.group_details, name='group_details'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('notifications/', views.notifications, name='notifications'),
    path('post_comment/<int:post_id>/', views.post_comment, name='post_comment'), 
    path('post_create/', views.post_create, name='post_create'),
    path('post_details/<int:post_id>/', views.post_details, name='post_details'),  
    path('post_edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('post_like/<int:post_id>/', views.post_like, name='post_like'),
    path('post_remove/<int:post_id>/', views.post_remove, name='post_remove'),
    path('private_messages/', views.private_messages, name='private_messages'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('signup/', views.signup_view, name='signup_view'),
    path('user_profile/<int:user_id>/update_field/', views.user_profile_field_update, name='user_profile_field_update'),
    path('user_profile_image/<int:user_id>/', views.user_profile_image, name='user_profile_image'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_feed', views.user_feed, name='user_feed'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# --------- CB 4 - VIEWS ---------
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
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import Comment, Post, Profile, FriendList, FriendRequest, Notification, Group, GroupMember, Message

# VIEW 1 - HOME 
def index(request):
    if request.user.is_authenticated:
        post_list = Post.objects.all().order_by('-timestamp')
        paginator = Paginator(post_list, 10)  # Show 10 posts per page

        page = request.GET.get('page')
        posts = paginator.get_page(page)

        friends_sent = FriendRequest.objects.filter(sender=request.user, status='accepted')
        friends_received = FriendRequest.objects.filter(recipient=request.user, status='accepted')
        friends = [fr.from_user for fr in friends_received] + [fr.to_user for fr in friends_sent]

        latest_posts = Post.objects.filter(author__in=friends).order_by('-timestamp')[:10]

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
    posts = Post.objects.filter(author__in=friends + [request.user]).order_by('-timestamp')
    
    # Adding pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
    }
    return render(request, 'user_feed.html', context)
# VIEW 5 - LOGGED-IN - PROFILE
@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)
    user_posts = Post.objects.filter(author=user).order_by('-timestamp')
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
@csrf_exempt
@login_required
def user_profile_field_update(request, user_id):
    if request.method == 'POST' and request.is_ajax():
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')

        if field_name in ['bio', 'gender', 'profession']:
            user_profile = Profile.objects.get(user__id=user_id)
            setattr(user_profile, field_name, field_value)
            user_profile.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid field"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"})
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
# VIEW 13 - POST: EDIT
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user_feed')
    else:
        form = PostForm(instance=post)

    context = {'form': form, 'post': post}
    return render(request, 'post_edit.html', context)
# VIEW 14 - POST: REMOVE
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
# VIEW 15 - POST: LIST
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'post_list.html', {'posts': posts})
# --------- VIEW 16 - FRIEND REQUEST ---------
@login_required
def friend_request(request):
    pending_friend_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')
    
    return render(request, 'friend_request.html', {'pending_friend_requests': pending_friend_requests})
# VIEW 17 - FRIENDSHIPS
def friendships(user):
    friends_sent = FriendRequest.objects.filter(sender=user, status='accepted')
    friends_received = FriendRequest.objects.filter(recipient=user, status='accepted')
    friends = [fr.recipient for fr in friends_sent] + [fr.sender for fr in friends_received]
    return friends
# VIEW 18 - FRIEND REQUEST: ACCEPT
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
# VIEW 19 - FRIEND REQUEST: REJECT
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
# VIEW 20 - FRIEND LIST 
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
# VIEW 21 - NOTIFICATIONS
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})
# VIEW 22 - PRIVATE MESSAGES
@login_required
def private_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'private_messages.html', {'sent_messages': sent_messages, 'received_messages': received_messages})
# VIEW 23 - GROUPS
@login_required
def groups(request):
    group_memberships = GroupMember.objects.filter(user=request.user)
    return render(request, 'groups.html', {'group_memberships': group_memberships})
# VIEW 24 - GROUPS DETAILS
@login_required
def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = GroupMember.objects.filter(group=group)
    return render(request, 'group_details.html', {'group': group, 'group_members': group_members})


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


# --------- CB 10 - HTML/JS FILES ---------
# ALL THE HTML TEMPLATES USED IN THE SOCIAL NETWORKING PROJECT

# 1: base.html
# 2: error_page.html
# 3: footer.html
# 4: forgot_password
# 5: friend_list.html
# 6: group_details.html
# 7: groups.html
# 8: header_logged_in.html
# 9: header_not_logged_in.html
# 10: index.html
# 11: notifications.html
# 12: post_comment.html
# 13: post_create.html
# 14: post_details.html
# 15: post_edit.html
# 16: post_list.html
# 17: post_remove.html
# 18: private_messages.html
# 19: search_results.html
# 20: signup.html
# 20: user_feed.html
# 21: user_profile.html
# 22: user_profile_image.html

# JAVASCRIPT-FILES USED 
# 1: script.js