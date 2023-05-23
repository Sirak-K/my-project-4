# File: views.py

import json, traceback
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from django.views.generic import TemplateView, View, UpdateView, DeleteView, CreateView, ListView, DetailView
from .forms import UserSearchForm, CommentForm, PostForm, PostEditForm, UpdateProfileForm, UpdateProfileImageForm
from .models import models, User, Friendship, Comment, Post, Profile


# VIEW 1 - SIGN-UP
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
            return redirect('user_feed') 
    else:
        # If it's not a POST request, create an empty form
        form = UserCreationForm()
    # Render the signup template with the form
    return render(request, 'signup.html', {'form': form})
# VIEW 2 - LOG-IN
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
# VIEW 3 - [ LOG-OUT ] 
def logout_view(request):
    logout(request)
    return redirect('login')
# VIEW 4 - HOME [ LOGGED-IN ] --------->
@login_required
def index(request):
   
    return render(request, 'user_feed.html')

# VIEW 5 - USER FEED (displays posts)
@login_required
def user_feed(request):
    user = request.user
    friend_ids = Friendship.objects.filter(
        Q(sender=user, status='accepted') | Q(receiver=user, status='accepted')
    ).values_list('sender_id', 'receiver_id')

    # Include the logged-in user's own posts
    friend_ids = [friend_id for friend_id in friend_ids for friend_id in friend_id]
    friend_ids.append(user.id)

    all_posts = Post.objects.filter(post_author_id__in=friend_ids).order_by('-post_created_at')
    all_post_comments = Comment.objects.all().order_by('-comment_created_at')

    return render(request, 'user_feed.html', {'all_posts': all_posts, 'all_post_comments': all_post_comments})




# VIEW 6 - USER PROFILE (also displays posts)
class UserProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'user_profile.html'
    
    # Update the get_object method to accept a username from the URL
    def get_object(self, queryset=None):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return user.profile

    def get_success_url(self):
        username = self.kwargs['username']
        return reverse_lazy('user_profile', kwargs={'username': username})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_profile = get_object_or_404(Profile, user=user)
        friends = Friendship.objects.filter(
            Q(sender=user, status='accepted') | Q(receiver=user, status='accepted')
        )
        friendship = Friendship.objects.filter(sender=user, receiver=user_profile.user).first()
        sent_friend_requests = Friendship.objects.filter(sender=user, status='pending')
        received_friend_requests = Friendship.objects.filter(receiver=user, status='pending')

        profile_data = {
            'user_profile': user_profile,
            'friends': friends,
            'friendship': friendship,
            'sent_friend_requests': sent_friend_requests,
            'received_friend_requests': received_friend_requests,
        }

        friend_ids = friends.values_list('sender_id', 'receiver_id')
        friend_ids = [friend_id for friend_id in friend_ids for friend_id in friend_id]
        friend_ids.append(user.id)
        all_posts = Post.objects.filter(post_author_id__in=friend_ids).order_by('-post_created_at')

        post_data = {'all_posts': all_posts}

        return {**profile_data, **post_data}

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)




   
   
   
    # Retrieve search query from request body

# data: stores the result of parsing the request body as JSON data.
# search_query: stores the value of the 'search_query' key from the parsed JSON data. It represents the search query input by the user.
# json.loads(): converts the JSON-formatted request body into a Python object.
# request.body: the raw request body that contains the data sent by the client.
    
# The get method is responsible for handling HTTP GET requests, 
# which are commonly used for retrieving and displaying information. 


# VIEW 6 - USER SEARCH 
class UserSearchView(View):
    template_name = 'user_search.html'

    def get(self, request):
        # Display the user search form

        form = UserSearchForm(request.GET)
       
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            data = json.loads(request.body)
            search_query = data['search_query']
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing search_query parameter'}, status=400)

        searched_users = User.objects.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        )
        response_data = {
            'users': list(searched_users.values()),
        }
        return JsonResponse(response_data)







# VIEW 7 - LOGGED-IN - PROFILE - UPLOAD IMAGES
@login_required
def user_profile_image(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = UpdateProfileImageForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile image and banner updated successfully.')
            # Store the updated user profile image URL in the session
            request.session['user_profile_image_url'] = user_profile.profile_image.url if user_profile.profile_image else None
            return redirect('user_feed')
    else:
        form = UpdateProfileImageForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'user_profile_image.html', context)

# VIEW 8 - LOGGED-IN - PROFILE - UPDATE PROFILE DETAILS
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





# VIEW  - FRIEND REQUESTS
class FriendRequestView(CreateView):
    model = Friendship
    fields = []

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username': self.receiver.username})  # Replace with your URL pattern name

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = self.get_receiver() 
        return super().form_valid(form)
# VIEW 10 - FRIEND LIST
class FriendListView(ListView):
    model = Friendship
    template_name = 'friend_list.html'

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(Q(sender=user) | Q(receiver=user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['friends'] = Friendship.objects.filter(Q(sender=user, status='accepted') | Q(receiver=user, status='accepted'))
        context['sent_friend_requests'] = Friendship.objects.filter(sender=user, status='pending')
        context['received_friend_requests'] = Friendship.objects.filter(receiver=user, status='pending')
        return context
# VIEW 11 - Friendship - ACCEPT
class FriendAcceptView(UpdateView):
    model = Friendship
    template_name = 'friend_accept.html'
    fields = []

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = 'accepted'
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('friend_list')
# VIEW 12 - Friendship - REJECT
class FriendRejectView(UpdateView):
    model = Friendship
    template_name = 'friend_reject.html'
    fields = []

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = 'rejected'
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('friend_list')
# VIEW 13 - Friendship - CANCEL
class FriendCancelView(UpdateView):
    model = Friendship
    template_name = 'friend_cancel.html'
    fields = []

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = 'canceled'
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('friend_list')


# VIEW 14  - Post List
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list_context'
# VIEW 15  - Post Details
class PostDetailsView(DetailView):
    model = Post
    # Byt ej template_name annars kmr inte rendera CSS i single-post views
    template_name = 'post_details_page.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.is_friend(request.user, self.object.post_author):
            # Handle the case where the user is not a friend of the post author
            return HttpResponseForbidden("You are not authorized to view this post.")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def is_friend(self, user, author):
        if user == author:
            return True  # Allow the author to view their own post
        return Friendship.objects.filter(
            (Q(sender=user, receiver=author) | Q(sender=author, receiver=user)),
            status='accepted'
        ).exists()

    

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details_page', pk=post.pk)
        else:
            # Handle form errors if needed
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments_for_post.order_by('comment_created_at')
        context['all_post_comments'] = comments
        return context
# VIEW 16  - Post Create
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('user_feed')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_image = self.request.user.profile.profile_image.url if self.request.user.profile.profile_image else '/static/default_profile_image.jpg'
        context['profile_image'] = profile_image
        return context

    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super().form_valid(form)
# VIEW 17 - Post Delete
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('user_feed')
# VIEW 18 - Comment Create
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post_comment_create.html'  
    success_url = reverse_lazy('user_feed')

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.comment_on_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        super().form_valid(form)
        return redirect('post_details_page', pk=self.kwargs['pk'])
# VIEW 19 - Post Like
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.is_liked_by_user(user):
        post.post_likes.remove(user)
        post_like_status = False
    else:
        post.post_likes.add(user)
        post_like_status = True

    response = {
        'post_like_status': post_like_status,
        'like_count': post.post_likes.count()
    }
    return JsonResponse(response)

