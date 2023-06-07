# File: views.py

import json, traceback, logging
logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import RedirectView, TemplateView, FormView, View, UpdateView, DeleteView, CreateView, ListView, DetailView
from .forms import  CustomUserCreationForm, FriendRequestForm, UserSearchForm, CommentForm, PostForm, PostEditForm, UpdateProfileForm, UpdateProfileImageForm
from .models import User, FriendRequest, Friendship, Comment, Post, Profile, models

# VIEW 0 - AUTHENTICATION
# - API-Endpoint
class LoginRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# VIEW 1 - SIGNUP
# - POST, REDIRECT
class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = 'user_feed'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# VIEW 2 - LOGIN
# - GET, POST, REDIRECT
class LoginView(View):
    template_name = 'login.html'
    success_url = 'user_feed'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        else:
            messages.error(request, 'The provided username or password is incorrect.')
            return render(request, self.template_name)   

# VIEW 3 - LOGOUT
# - REDIRECT
class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

# VIEW 4 - INDEX
# - GET, HTML/TEMPLATE
class IndexView(TemplateView):
    template_name = 'user_feed.html'


# VIEW - USER FEED (displays posts of logged-in user and his friends)
# - GET, HTML/TEMPLATE
class UserFeedView(LoginRequiredMixin, ListView):
    template_name = 'user_feed.html'
    context_object_name = 'all_posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        friends = Friendship.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user),
            status='accepted'
        ).values_list('sender', 'receiver')

        friend_ids = list(set([friend_id for friendship in friends for friend_id in friendship]))

        return Post.objects.filter(
            models.Q(post_author=user) | models.Q(post_author_id__in=friend_ids)
        ).order_by('-post_created_at')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        user_friends = user_profile.get_friends()
        context['user_friends'] = user_friends

        context['all_post_comments'] = Comment.objects.all().order_by('-comment_created_at')
        return context


# VIEW - USER PROFILE (displays only posts of logged-in user)
class UserProfileView(LoginRequiredMixin, View):
    model = Profile
    fields = []
    template_name = 'user_profile.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        if username is None:
            return self.request.user.profile
        else:
            user = get_object_or_404(User, username=username)
            return user.profile

    def get_success_url(self):
        username = self.kwargs['username']
        return reverse_lazy('user_profile', kwargs={'username': username})

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if username and username != self.request.user.username:
            user = get_object_or_404(User, username=username)
            user_profile = user.profile
        else:
            user_profile = self.request.user.profile

        all_posts = Post.objects.all().order_by('-post_created_at')

        # Get the receiver ID from the user's profile
        receiver_id = user_profile.user_id

        # Create instances of the forms
        friend_request_form = FriendRequestForm()
        post_form = PostForm()
        post_edit_form = PostEditForm()
        comment_form = CommentForm()

        context = {
            'post_form': post_form,
            'post_edit_form': post_edit_form,
            'comment_form': comment_form,
            'all_posts': all_posts,

            'friend_request_form': friend_request_form,
            'receiver_id': receiver_id,

            'is_owner': user_profile.user == request.user,
            'user_profile': user_profile,
            'user_profile_image_url': user_profile.profile_image.url if user_profile.profile_image else '/media/img/default_profile_image.png',
            'user_profile_banner_url': user_profile.banner_image.url if user_profile.banner_image else '/media/img/default_banner_image.png',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'send_friend_request' in request.POST:
            user_profile = self.get_object()
            receiver_id = user_profile.user_id
            friendship_manager = FriendshipManager()
            return friendship_manager.send_friend_request(request, receiver_id=receiver_id)
        elif 'create_post' in request.POST:
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.post_author = request.user
                post.save()
                return redirect('user_profile', username=request.user.username)
        return super().post(request, *args, **kwargs)



# VIEW - USER DELETION & USER DELETION CONFIRMATION
class UserDeletionView(LoginRequiredMixin, TemplateView):
    template_name = 'user_deletion_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        confirm = request.POST.get('confirm')
        if confirm == 'yes':
            user = request.user
            user.delete()
            logout(request)
            return redirect('login')  # Redirect to home or any other desired page
        elif confirm == 'no':
            return redirect('user_profile', username=request.user.username)





# VIEW - USER PROFILE DETAILS
class UserProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'user_profile_details.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            user = get_object_or_404(User, username=username)
            return user.profile
        else:
            return self.request.user.profile
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context






# VIEW - USER PROFILE - IMAGE AND PROFILE BANNER
class UserProfileImageView(LoginRequiredMixin, FormView):
    template_name = 'user_profile_image.html'
    form_class = UpdateProfileImageForm

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.save()
        user_profile = self.request.user.profile
        self.request.session['user_profile_image_url'] = user_profile.profile_image.url if user_profile.profile_image else None
        self.request.session['user_profile_banner_url'] = user_profile.banner_image.url if user_profile.banner_image else None
        messages.success(self.request, 'Profile image and banner updated successfully.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})
# VIEW  - USER PROFILE - UPDATE PROFILE
# - POST, JSON
class UserProfileFieldUpdateView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")

            field_name = data.get('fieldName')
            field_value = data.get('value')
            if field_name in ['bio', 'gender', 'profession']:
                user_profile = Profile.objects.get(user__id=user_id)
                setattr(user_profile, field_name, field_value)
                user_profile.save()
                messages.success(request, 'Profile updated successfully.')
                return JsonResponse({"status": "success"})
            else:
                return HttpResponseBadRequest(f"The field '{field_name}' is not a valid field for updating.")
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            return JsonResponse({"status": "error", "message": str(e)})
# VIEW  - USER SEARCH
# - GET, POST, JSON
class UserSearchView(LoginRequiredMixin, View):
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

# VIEW - FRIENDSHIP MANAGER
class FriendshipManager(View):
    def send_friend_request(self, request, receiver_id):
        try:
            receiver = User.objects.get(id=receiver_id)
            sender = request.user  # Use the logged-in user as the sender

            if receiver:
                print("[DEBUG]: Sender:", sender.username)
                print("[DEBUG]: Receiver:", receiver.username)

                friend_request = FriendRequest(sender=sender, receiver=receiver)
                friend_request.save()

                print("[DEBUG]: Friend request sent successfully.")
                print(f"{sender.username} sent a friend request to {receiver.username}")

                return redirect('friend_list')
            else:
                print("[DEBUG]: Receiver does not exist.")
                return HttpResponseBadRequest("Receiver does not exist")
        except User.DoesNotExist:
            print("[DEBUG]: Receiver does not exist.")
            return HttpResponseBadRequest("Receiver does not exist")
    def cancel_friend_request(self, request, request_id=None, **kwargs):
        print("[DEBUG]: cancel_friend_request method called")
        if request.method == 'POST':
            try:
                friend_request = FriendRequest.objects.get(id=request_id)

                print("[DEBUG]: Sender:", friend_request.sender.username)
                print("[DEBUG]: Logged-in User:", request.user.username)

                if friend_request.sender == request.user:
                    friend_request.cancel()

                    print("[DEBUG-2]: CANCELED Friend Requests - Friend request canceled successfully.")
                    return redirect('friend_list')
                else:
                    # Handle the case where the logged-in user is not the sender of the friend request
                    return HttpResponseBadRequest("You are not the sender of this friend request.")
            except FriendRequest.DoesNotExist:
                # Handle the case where the friend request doesn't exist
                return HttpResponseBadRequest("Friend request does not exist.")
        else:
            return HttpResponseBadRequest("Invalid request method")
    def reject_friend_request(self, request, request_id=None, **kwargs):
        if request.method == 'POST':
            try:
                friend_request = FriendRequest.objects.get(id=request_id)

                if friend_request.receiver == request.user:
                    friend_request.delete()

                    print("Friend request rejected successfully.")
                    return redirect('friend_list')
                else:
                    # Handle the case where the logged-in user is not the receiver of the friend request
                    return HttpResponseBadRequest("You are not the receiver of this friend request.")
            except FriendRequest.DoesNotExist:
                # Handle the case where the friend request doesn't exist
                return HttpResponseBadRequest("Friend request does not exist.")
        else:
            return HttpResponseBadRequest("Invalid request method")
    def accept_friend_request(self, request, request_id=None, **kwargs):
        print("[DEBUG]: accept_friend_request method called")
        if request.method == 'POST':
            try:
                friend_request = FriendRequest.objects.get(id=request_id)

                if friend_request.receiver == request.user:
                    friend_request.accept()
                    

                    # Create the friendship object before deleting the friend request
                    Friendship.objects.create(sender=friend_request.sender, receiver=friend_request.receiver)
                    print("Friendship CREATED.")

                    

                    return redirect('friend_list')
                else:
                    # Handle the case where the logged-in user is not the receiver of the friend request
                    return HttpResponseBadRequest("You are not the receiver of this friend request.")
            except FriendRequest.DoesNotExist:
                # Handle the case where the friend request doesn't exist
                return HttpResponseBadRequest("Friend request does not exist.")
        else:
            return HttpResponseBadRequest("Invalid request method")
    def get_received_friend_requests(self, request, receiver_id):
        received_friend_requests = FriendRequest.objects.filter(receiver_id=receiver_id)

        print("friend_list retrieved: RECEIVED ")
        return received_friend_requests
    def get_sent_friend_requests(self, request):
        sent_friend_requests = FriendRequest.objects.filter(sender=request.user)
        print("friend_list retrieved: SENT")
        return sent_friend_requests
    




    def get_existing_friendships(self, request):
        
        existing_friendships = Friendship.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

        return existing_friendships


    def remove_friendship(self, request, friendship_id=None):
        try:
            # Get the friendship object
            print("Friendship ID:", friendship_id)
            friendship = Friendship.objects.get(id=friendship_id)

            # Check if the logged-in user is part of the friendship
            if friendship.sender == request.user or friendship.receiver == request.user:
                # Delete the friendship object
                friendship.delete()
                print("[DEBUG-7]: Friendship Deletion - Friendship deleted successfully.")
                return redirect('friend_list')
            else:
                # Handle the case where the logged-in user is not part of the friendship
                return HttpResponseBadRequest("You are not part of this friendship.")
        except Friendship.DoesNotExist:
            # Handle the case where the friendship doesn't exist
            # Redirect to an appropriate error page or display an error message
            return HttpResponseBadRequest("Friendship does not exist.")

    
    def get(self, request):
        # Ensure that the user_profile object is correctly initialized and obtained
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # Handle the case where the user_profile doesn't exist
            return HttpResponseBadRequest("User profile does not exist")

        # Get the receiver ID from the user's profile
        receiver_id = user_profile.user.id

        
        sent_friend_requests = self.get_sent_friend_requests(request)
        received_friend_requests = self.get_received_friend_requests(request, receiver_id)
        existing_friendships = self.get_existing_friendships(request)
        
        context = {

            'receiver_id': receiver_id,
            'sent_friend_requests': sent_friend_requests,
            'received_friend_requests': received_friend_requests,
            'existing_friendships': existing_friendships,
        }

        return render(request, 'friend_list.html', context)


    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'send_friend_request':
            # receiver_id = int(receiver_id)
            receiver_id = request.POST.get('receiver')
            return self.send_friend_request(request, receiver_id)
        elif action == 'accept_friend_request':
            request_id = kwargs.get('request_id')
            return self.accept_friend_request(request, request_id=request_id)  # Pass request_id as a keyword argument
        elif action == 'reject_friend_request':
            request_id = kwargs.get('request_id')
            return self.reject_friend_request(request, request_id)
        elif action == 'cancel_friend_request':
            request_id = kwargs.get('request_id')
            return self.cancel_friend_request(request, request_id)
        elif action == 'remove_friendship':
            friendship_id = kwargs.get('friendship_id')
            return self.remove_friendship(request, friendship_id)
        else:
            # Handle invalid action
            return HttpResponseBadRequest("Invalid action")

# VIEW - Post Details
# - GET, POST, REDIRECT, HTML/TEMPLATE
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

        author_profile_image = post.post_author.profile.profile_image.url if post.post_author.profile.profile_image else '/media/img/default_profile_image.png'
        context['author_profile_image'] = author_profile_image
        
        context['all_post_comments'] = comments
        return context
# VIEW - Post Create
# - POST, HTML/TEMPLATE
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('user_feed')


    def form_valid(self, form):
        profile = self.request.user.profile
        form.instance.post_author_image = profile.profile_image
        form.instance.post_author = self.request.user
        return super().form_valid(form)
# VIEW - Post List
# - GET, HTML/TEMPLATE
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list_context'
# VIEW 18 - Post Delete
# - POST, HTML/TEMPLATE
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('user_feed')
# VIEW 19 - Post Like
# - POST, AJAX, JSON
class PostLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
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
# VIEW 20 - Comment Create
# - POST, HTML/TEMPLATE
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



