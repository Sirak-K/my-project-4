from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, UpdateProfileImageForm
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

    context = {'user_profile': user_profile, 'user_posts': user_posts, 'friends': friends}
    return render(request, 'user_profile.html', context)

# VIEW X - LOGGED-IN - PROFILE - UPLOAD IMAGES
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


# ---------> VIEW 6 - [ LOG-OUT ] --------->
def logout_view(request):
    logout(request)
    return redirect('login_view')
# VIEW 7 - POST: CREATE
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
# VIEW 8 - POST: COMMENTS
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
# VIEW 9 - POST: LIKES
@require_POST
def post_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({"likes": post.likes})
    else:
        return HttpResponseNotAllowed(['POST'])
# VIEW 10 - POST: DETAILS
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'post_details.html', {'post': post, 'comments': comments})
# VIEW 11 - POST: EDIT
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
# VIEW 12 - POST: REMOVE
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
# VIEW 13 - POST: LIST
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'post_list.html', {'posts': posts})
# --------- VIEW 14 - FRIEND REQUEST ---------
@login_required
def friend_request(request):
    pending_friend_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')
    
    return render(request, 'friend_request.html', {'pending_friend_requests': pending_friend_requests})
# VIEW 15 - FRIENDSHIPS
def friendships(user):
    friends_sent = FriendRequest.objects.filter(sender=user, status='accepted')
    friends_received = FriendRequest.objects.filter(recipient=user, status='accepted')
    friends = [fr.recipient for fr in friends_sent] + [fr.sender for fr in friends_received]
    return friends
# VIEW 16 - FRIEND REQUEST: ACCEPT
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
# VIEW 17 - FRIEND REQUEST: REJECT
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
# VIEW 18 - FRIEND LIST 
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
# VIEW 19 - NOTIFICATIONS
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})
# VIEW 20 - PRIVATE MESSAGES - VIEW
@login_required
def private_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'private_messages.html', {'sent_messages': sent_messages, 'received_messages': received_messages})
# VIEW 21 - GROUPS - VIEW
@login_required
def groups(request):
    group_memberships = GroupMember.objects.filter(user=request.user)
    return render(request, 'groups.html', {'group_memberships': group_memberships})
# VIEW 22 - GROUP DETAILS - VIEW
@login_required
def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = GroupMember.objects.filter(group=group)
    return render(request, 'group_details.html', {'group': group, 'group_members': group_members})

