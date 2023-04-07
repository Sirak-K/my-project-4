
# "CB" = CODEBASE

# --------- CB 1 - ADMIN ---------
from django.contrib import admin
from .models import Post, Profile, FriendList, FriendRequest, Notification, Group, GroupMember, Message
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Message)


# --------- CB 2 - APPS --------- 
from django.apps import AppConfig
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
def ready(self):
        import core.signals


# --------- CB 3 - FORMS ---------
from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'privacy_settings']


# --------- CB 4 - SIGNALS ---------
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


# --------- CB 5 - URLS 1 ---------
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
    path('friend_list/', views.friend_list, name='friend_list'),
    path('friend_request/', views.friend_request, name='friend_request'),
    path('notifications/', views.notifications, name='notifications'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/', views.group_details, name='group_details'),
    path('private_messages/', views.private_messages, name='private_messages'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


# --------- CB 6 - URLS 2 ---------
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

# --------- CB 7 - MODELS ---------
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
# DECORATOR 1 - CREATE PROFILE
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# MODEL 2 - POST
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key relationship with User
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    privacy_settings = models.CharField(max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the post is created
    def __str__(self):
        return f"{self.author.username}'s Post"
# MODEL 3 - COMMENT
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author.username}'s Comment"
# MODEL 4 - LIKE
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} liked {self.post.author.username}'s Post"
# MODEL 5 - FRIEND LIST
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    status = models.CharField(max_length=20)  # "Pending", "Accepted", "Rejected"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} sent a friend request to {self.recipient.username}"
# MODEL 6 - FRIEND LIST
class FriendList(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_lists_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_lists_user2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username} are friends"
# MODEL 7 - NOTIFICATION
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)  # "friend_request", "like", "comment", etc.
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Set to False by default
    def __str__(self):
        return f"{self.user.username}'s {self.type} Notification"
# MODEL 8 - PRIVATE MESSAGES 
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender.username} sent a message to {self.recipient.username}"
# MODEL 9 - GROUP
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} Group"
# MODEL 10 - GROUP MEMBERS
class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} is a member of {self.group.name}"
# MODEL 11 - GROUP POSTS
class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='group_posts/', blank=True, null=True)
    video = models.FileField(upload_to='group_videos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author.username}'s Post in {self.group.name} Group"


# --------- CB 8 - VIEWS ---------
from .forms import PostForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, FriendList, FriendRequest, Notification, Group, GroupMember, Message

# VIEW 1 - HOME
@login_required
def home(request):
    post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, 10) # Show 10 posts per page

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    # New code
    friends_sent = FriendRequest.objects.filter(sender=request.user, status='accepted')
    friends_received = FriendRequest.objects.filter(recipient=request.user, status='accepted')
    friends = [fr.from_user for fr in friends_received] + [fr.to_user for fr in friends_sent]
    
    latest_posts = Post.objects.filter(author__in=friends).order_by('-timestamp')[:10]
    
    context = {
        'posts': posts,
        'latest_posts': latest_posts
    }
    return render(request, 'home.html', context)
# VIEW 2 - LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # or any other page you want to redirect the user to after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')
# VIEW 3 - PROFILE
@login_required
def user_profile(request, user_id):
    user_profile = get_object_or_404(Profile, user__id=user_id)
    friends = friends_list(request)

    context = {'profile': user_profile, 'friends': friends}
    return render(request, 'user_profile.html')
# VIEW 4 - NEW POST
@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})
# VIEW 5 - LIKE POST
@require_POST
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})
# VIEW 6 - FRIEND REQUEST
@login_required
def friend_request(request):
    pending_friend_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')
    
    return render(request, 'friend_request.html', {'pending_friend_requests': pending_friend_requests})
# VIEW 7 - FRIEND LIST
@login_required
def friend_list(request):
    friend_lists = FriendList.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friends = []

    for friend_list in friend_lists:
        if friend_list.user1 == request.user:
            friends.append(friend_list.user2)
        else:
            friends.append(friend_list.user1)

    return render(request, 'friend_list.html', {'friends': friends})
# VIEW 8 - NOTIFICATIONS
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})
# VIEW 9 - PRIVATE MESSAGES
@login_required
def private_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'private_messages.html', {'sent_messages': sent_messages, 'received_messages': received_messages})
# VIEW 10 - GROUPS
@login_required
def groups(request):
    group_memberships = GroupMember.objects.filter(user=request.user)
    return render(request, 'groups.html', {'group_memberships': group_memberships})
# VIEW 11 - GROUP DETAILS
@login_required
def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = GroupMember.objects.filter(group=group)
    return render(request, 'group_details.html', {'group': group, 'group_members': group_members})


# ALL HTML TEMPLATES

# HTML-1 : base.html
# HTML-2 : friend_list.html
# HTML-3 : group_details.html
# HTML-4 : group.html
# HTML-5 : home.html
# HTML-6 : login.html
# HTML-7 : logout.html
# HTML-8 : new_post.html
# HTML-9 : notifications.html
# HTML-10 : private_messages.html
# HTML-11 : show_posts.html
# HTML-12 : signup.html
# HTML-13 : user_profile.html