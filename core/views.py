import json
import logging
import traceback

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    RedirectView, TemplateView, FormView, View, DeleteView,
    CreateView, ListView, UpdateView, DetailView
)

from .forms import (
    CustomPasswordResetForm, CustomUserCreationForm, FriendRequestForm,
    UserSearchForm, CommentForm, PostForm, PostEditForm, UpdateProfileForm,
    UpdateProfileImageForm
)
from .models import (
    User, FriendRequest, Friendship, Comment, Post, Profile, models
)

logger = logging.getLogger(__name__)


# VIEW 0 - AUTHENTICATION
class LoginRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
# VIEW 1 - INDEX
class IndexView(TemplateView):
    template_name = 'user_feed.html'
# VIEW 2 - LOGIN
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
class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
# VIEW 4 - SIGNUP
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
# VIEW 5 - USER PROFILE - IMAGE AND PROFILE BANNER
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
# VIEW 6 - USER PROFILE - UPDATE PROFILE
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


# VIEW 7 - USER FEED (displays posts of logged-in user and his friends)
class UserFeedView(LoginRequiredMixin, ListView):
    template_name = 'user_feed.html'
    context_object_name = 'all_posts'
    paginate_by = 2

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

        all_posts = context['object_list']

        
        context['all_posts'] = all_posts
        context['all_post_comments'] = Comment.objects.all().order_by('-comment_created_at')
        context['user_friends'] = user_friends
      
        return context





# VIEW 8 - USER PROFILE (displays only the posts that the logged-in user has created)
class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'user_profile.html'
    context_object_name = 'all_posts'
    paginate_by = 2

    def get_queryset(self):
        user_profile = self.get_user_profile()
        return Post.objects.filter(post_author=user_profile.user).order_by('-post_created_at')

    def get_user_profile(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            return user.profile
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_user_profile()

        context['user_profile'] = user_profile
        context['all_post_comments'] = Comment.objects.all().order_by('-comment_created_at')
        context['post_form'] = PostForm()
        context['post_edit_form'] = PostEditForm()
        context['comment_form'] = CommentForm()
        context['is_owner'] = user_profile.user == self.request.user
        context['user_profile_image_url'] = user_profile.profile_image.url if user_profile.profile_image else '/media/img/default_profile_image.png'
        context['user_profile_banner_url'] = user_profile.banner_image.url if user_profile.banner_image else '/media/img/default_banner_image.png'
        context['friend_request_form'] = FriendRequestForm()
        context['receiver_id'] = user_profile.user_id

        # Check if the logged-in user and the user_profile are already friends
        are_friends = Friendship.objects.filter(
            (Q(sender=self.request.user) & Q(receiver=user_profile.user)) |
            (Q(sender=user_profile.user) & Q(receiver=self.request.user)),
            status='accepted'
        ).exists()
        context['are_friends'] = are_friends

        return context

    def post(self, request, *args, **kwargs):
        if 'send_friend_request' in request.POST:
            user_profile = self.get_user_profile()
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



# VIEW 12 - POST LIST
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list_context'









# VIEW 14 - POST DETAILS
class PostDetailsView(DetailView):
    model = Post
    template_name = 'post_edit_page.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.is_friend(request.user, self.object.post_author):
            return HttpResponseForbidden("You are not authorized to view this post.")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def is_friend(self, user, author):
        if user == author:
            return True  
        return Friendship.objects.filter(
            (Q(sender=user, receiver=author) | Q(sender=author, receiver=user)),
            status='accepted'
        ).exists()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_post_edit_page'] = True
        context['all_posts'] = Post.objects.all().order_by('-post_created_at')
        context['all_post_comments'] = Comment.objects.all().order_by('-comment_created_at')
      
        return context




# VIEW 9 - USER PROFILE DETAILS
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
# VIEW 10 - USER SEARCH
class UserSearchView(LoginRequiredMixin, View):
    template_name = 'user_search.html'

    def get(self, request):
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
# VIEW 11 - USER DELETION & USER DELETION CONFIRMATION
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
            return redirect('login') 
        elif confirm == 'no':
            return redirect('user_profile', username=request.user.username)



# VIEW 15 - POST EDIT PAGE
class PostEditView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'post_edit_page.html'
    context_object_name = 'post'
    success_url = reverse_lazy('user_feed')
      
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        post = Post.objects.get(pk=self.kwargs['pk'])
        kwargs['instance'] = post
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)
        post_content = form.cleaned_data['post_content']  # Get the updated post content
        post.post_content = post_content  # Update the post content
        post.save()  # Save the post
        print('[DEBUG]: Post Edit:, { post_content } updated successfully')
        return redirect('user_feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all() 
        return context





# VIEW 15 - POST CREATE
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





# VIEW 16 - POST DELETE
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('user_feed')

# VIEW xx - POST LIKE
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

# VIEW 17 - COMMENT CREATE
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




# VIEW 18 - FRIENDSHIP MANAGER
class FriendshipManager(View):
    def send_friend_request(self, request, receiver_id):
        try:
            receiver = User.objects.get(id=receiver_id)
            sender = request.user

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
                    return HttpResponseBadRequest("You are not the sender of this friend request.")
            except FriendRequest.DoesNotExist:
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
                    return HttpResponseBadRequest("You are not the receiver of this friend request.")
            except FriendRequest.DoesNotExist:
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
    
                    Friendship.objects.create(sender=friend_request.sender, receiver=friend_request.receiver)
                    print("Friendship CREATED.")

                    return redirect('friend_list')
                else:
                    return HttpResponseBadRequest("You are not the receiver of this friend request.")
            except FriendRequest.DoesNotExist:
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
            print("Friendship ID:", friendship_id)
            friendship = Friendship.objects.get(id=friendship_id)

            if friendship.sender == request.user or friendship.receiver == request.user:
                friendship.delete()
                print("[DEBUG-7]: Friendship Deletion - Friendship deleted successfully.")
                return redirect('friend_list')
            else:
                return HttpResponseBadRequest("You are not part of this friendship.")
        except Friendship.DoesNotExist:
            return HttpResponseBadRequest("Friendship does not exist.")

    
    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return HttpResponseBadRequest("User profile does not exist")

        receiver_id = user_profile.user.id
        sent_friend_requests = self.get_sent_friend_requests(request)
        existing_friendships = self.get_existing_friendships(request)
        received_friend_requests = self.get_received_friend_requests(request, receiver_id)
        
        context = {
            'receiver_id': receiver_id,
            'existing_friendships': existing_friendships,
            'sent_friend_requests': sent_friend_requests,
            'received_friend_requests': received_friend_requests,
        }

        return render(request, 'friend_list.html', context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'send_friend_request':
            receiver_id = request.POST.get('receiver')
            return self.send_friend_request(request, receiver_id)
        elif action == 'accept_friend_request':
            request_id = kwargs.get('request_id')
            return self.accept_friend_request(request, request_id=request_id)
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
            return HttpResponseBadRequest("Invalid action")
# VIEW 19 - PASSWORD RESET 
class PasswordResetView(View):
    template_name = 'password_reset_page.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('login')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 != new_password2:
                print('new_password2', 'New passwords do not match.')
                return self.form_invalid(form)

            username = form.cleaned_data['username']
            print("Username:", username)  # Debugging statement
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                print('username', 'Invalid username.')
                return self.form_invalid(form)

            print("User found:", user)  # Debugging statement

            user.set_password(new_password1)
            user.save()

            profile = user.profile
            profile.user.set_password(new_password1)
            profile.user.save()

            print("Password reset successful!")  # Debugging statement

            # Handle the response here, such as redirecting or rendering a success page
            return redirect(self.success_url)

        # Form is invalid
        return self.form_invalid(form)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
