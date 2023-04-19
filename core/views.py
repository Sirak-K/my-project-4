import json
import traceback  

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
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Comment, Post, Profile, FriendRequest, FriendList


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

        context = {
            'posts': posts,
            'post_details': Post.objects.all(),
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
# VIEW 8 - POST: CREATE
@login_required
def post_create(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'post_create.html', {'form': form, 'posts': posts})

# VIEW 9 - POST: DETAILS
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Create an instance of the CommentForm
    comment_form = CommentForm()

    # Pass the post_id value to the template context
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'post_id': post_id,
    }

    return render(request, 'post_details.html', context)


# VIEW 10 - POST: LIKES
@require_POST
def post_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({"likes": post.likes})
    else:
        return HttpResponseNotAllowed(['POST'])
# VIEW 11 - POST: COMMENTS
@csrf_exempt
@require_POST
def post_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get('content', '')
        if content:
            post = Post.objects.get(pk=post_id)
            comment = Comment(content=content, user=request.user, post=post)
            comment.save()
            return JsonResponse({"status": "success"})  # Return a JSON response instead of redirecting
        else:
            return JsonResponse({"status": "error", "message": "Content is empty"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})
# VIEW 12 - POST: COMMENTS LIST (SHOW)
def post_comment_list(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'post_comment_list.html', {'post': post, 'comments': comments})
# VIEW 13 - POST: LIST
def post_list():
    posts = Post.objects.all().order_by('-created_at')
    data = {
        'posts': list(posts.values())
    }
    return JsonResponse(data)
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
# ---- VIEW 15 - FRIEND REQUEST ----
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
# ---------> VIEW 20 - [ LOG-OUT ] --------->
def logout_view(request):
    logout(request)
    return redirect('login_view')