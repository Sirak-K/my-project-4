import json
import traceback  

from django.template.loader import render_to_string

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import PostForm, CommentForm, UpdateProfileForm, UpdateProfileImageForm
from .models import Comment, Post, Profile, FriendRequest, FriendList

ITEMS_PER_PAGE = 10 

# VIEW 1 - SIGNUP
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
# VIEW 2 - LOGIN
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
                messages.error(request, 'The provided username or password is incorrect.')
                return render(request, 'login.html')
        else:
            logout(request) 
            return render(request, 'login.html')
# VIEW 3 - HOME [ LOGGED-IN ] --------->
@login_required
def index(request):
    post_list = Post.objects.all().order_by('-created_at')
    posts = fetch_paginated_posts(request, post_list)

    context = {
        'posts': posts,
    }
    return render(request, 'user_feed.html', context)
# VIEW 4 - LOGGED-IN - USER FEED
@login_required
def user_feed(request):
    friends = friendships(request.user)
    queryset = Post.objects.filter(author__in=friends + [request.user]).order_by('-created_at')
    posts = fetch_paginated_posts(request, queryset)

    context = {
        'posts': posts,
    }
    return render(request, 'user_feed.html', context)
# VIEW 5 - LOGGED-IN - PROFILE
@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)
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
            return HttpResponseBadRequest(f"The field '{field_name}' is not a valid field for updating.")
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        return JsonResponse({"status": "error", "message": str(e)})


# VIEW 8 - POST: CREATE
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # return redirect('post_details', post_id=post.id)
    else:
        form = PostForm()

    return render(request, 'user_feed.html', {'form': form})

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

    return render(request, 'post_details.html', context) # Added return statement
# VIEW 10 - POST: REMOVE
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


# VIEW 11 - POST: LIST
def post_list(request):
    page = request.GET.get('page', 1)
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    posts = paginator.get_page(page)
    # Get comments for each post and add them to the post object
    for post in posts:
        post.comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Render the post list using the Django template
    rendered_posts = render_to_string('user_feed.html', {
        'posts': posts,
        'current_page': page,
        'total_pages': paginator.num_pages
    })

    return render(request, rendered_posts, 'post_list.html', {'posts': posts, 'paginator': paginator})
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('user_feed')

    context = {'post': post}
    return render(request, 'post_remove.html', context)
# VIEW 12 - POST: LIST - FETCH AND DISPLAY POSTS (SHOULD BE REFACTORED TO BE COMBINED INTO post_list-view)
def fetch_paginated_posts(request, queryset):
    paginator = Paginator(queryset, ITEMS_PER_PAGE)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts


# VIEW 13 - POST: COMMENTS
@require_POST
def post_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get('content', '')
        if content:
            post = Post.objects.get(pk=post_id)
            comment = Comment(content=content, user=request.user, post=post)
            comment.save()
           
            return JsonResponse({"status": "success" })
# VIEW 14 - POST: COMMENTS LIST (SHOW)
def post_comment_list(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'post_comment_list.html', {'post': post, 'comments': comments})
# VIEW 15 - POST: LIKES
@require_POST
def post_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({"likes": post.likes}, safe=False)
    else:
        return HttpResponseNotAllowed(['POST'])


# ---- VIEW 16 - FRIENDSHIP ----
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
# ---------> VIEW 21 - [ LOG-OUT ] --------->
def logout_view(request):
    logout(request)
    return redirect('login_view')