from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, FriendRequest, Notification, Group, GroupMember, Message
from .forms import PostForm

# PAGE 1 - HOME
@login_required
def home(request):
    latest_posts = Post.objects.filter(author__in=request.user.profile.friends.all()).order_by('-timestamp')[:10]
    return render(request, 'home.html', {'latest_posts': latest_posts})

# PAGE 2 - PROFILE
@login_required
def user_profile(request, user_id):
    user_profile = get_object_or_404(Profile, user__id=user_id)
    return render(request, 'user_profile.html', {'profile': user_profile})

# PAGE 3 - NEW POST
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

# PAGE 4 - FRIENDS LIST
@login_required
def friends_list(request):
    friends = request.user.profile.friends.all()
    return render(request, 'friends_list.html', {'friends': friends})

# PAGE 5 - NOTIFICATIONS
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})

# PAGE 6 - PRIVATE MESSAGES
@login_required
def private_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'private_messages.html', {'sent_messages': sent_messages, 'received_messages': received_messages})

# PAGE 7 - GROUPS
@login_required
def groups(request):
    group_memberships = GroupMember.objects.filter(user=request.user)
    return render(request, 'groups.html', {'group_memberships': group_memberships})

# PAGE 8 - GROUP DETAILS
@login_required
def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = GroupMember.objects.filter(group=group)
    return render(request, 'group_details.html', {'group': group, 'group_members': group_members})

