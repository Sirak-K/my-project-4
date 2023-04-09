from .forms import PostForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, FriendList, FriendRequest, Notification, Group, GroupMember, Message

# VIEW 1 - HOME - 2 VIEWS
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
        return render(request, 'page_logged_in.html', context)
    else:
        return render(request, 'page_logged_out.html')
# VIEW 2 - SIGNUP - VIEW
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
            # Redirect the user to the home page
            return redirect('home')
    else:
        # If it's not a POST request, create an empty form
        form = UserCreationForm()
    # Render the signup template with the form
    return render(request, 'signup.html', {'form': form})


# VIEW 4 - LOGGED-IN - VIEW
@login_required
def logged_in_view(request):
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


# VIEW 5 - LOGGED-OUT - VIEW
def logged_out_view(request):
    if request.user.is_authenticated:
        return redirect('logged_in_view')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('logged_in_view')
            else:
                return render(request, 'page_logged_out.html', {'error': 'Invalid login credentials'})
        else:
            logout(request) 
            return render(request, 'page_logged_out.html')




# VIEW 6 - PROFILE - VIEW
@login_required
def user_profile(request, user_id):
    user_profile = get_object_or_404(Profile, user__id=user_id)
    friends = friend_list(request)

    context = {'profile': user_profile, 'friends': friends}
    return render(request, 'user_profile.html')
# VIEW 7 - NEW POST - VIEW
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
# VIEW 8 - LIKE POST
@require_POST
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})
# VIEW 9 - FRIEND REQUEST
@login_required
def friend_request(request):
    pending_friend_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')
    
    return render(request, 'friend_request.html', {'pending_friend_requests': pending_friend_requests})
# VIEW 10 - FRIEND LIST - VIEW
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
# VIEW 11 - NOTIFICATIONS
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})
# VIEW 12 - PRIVATE MESSAGES - VIEW
@login_required
def private_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'private_messages.html', {'sent_messages': sent_messages, 'received_messages': received_messages})
# VIEW 13 - GROUPS - VIEW
@login_required
def groups(request):
    group_memberships = GroupMember.objects.filter(user=request.user)
    return render(request, 'groups.html', {'group_memberships': group_memberships})
# VIEW 14 - GROUP DETAILS - VIEW
@login_required
def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = GroupMember.objects.filter(group=group)
    return render(request, 'group_details.html', {'group': group, 'group_members': group_members})

