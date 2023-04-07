# Here are some important views that you may want to add to your social network app:

# Friend request view: A view for sending friend requests to other users and accepting or rejecting friend requests.
# Group creation view: A view for creating new groups and adding members to them.
# Search view: A view for searching users, groups, posts, etc. based on keywords.
# Post detail view: A view for showing the details of a particular post, including its author, likes, comments, etc.
# Like/Unlike view: A view for allowing users to like or unlike posts.
# Comment view: A view for allowing users to add comments to posts.
# Profile edit view: A view for allowing users to edit their profile information, such as their bio, profile picture, etc.
# Group edit view: A view for allowing group owners to edit their group information, such as the group name, description, profile picture, etc.



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

# VIEW 7 - NOTIFICATIONS
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})

# VIEW 8 - PRIVATE MESSAGES
@login_required
def private_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'private_messages.html', {'sent_messages': sent_messages, 'received_messages': received_messages})

# VIEW 9 - GROUPS
@login_required
def groups(request):
    group_memberships = GroupMember.objects.filter(user=request.user)
    return render(request, 'groups.html', {'group_memberships': group_memberships})

# VIEW 10 - GROUP DETAILS
@login_required
def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = GroupMember.objects.filter(group=group)
    return render(request, 'group_details.html', {'group': group, 'group_members': group_members})

