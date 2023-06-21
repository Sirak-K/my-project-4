import json
import logging
import traceback

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
    UploadProfileImageForm
)
from .models import (
    User, FriendRequest, Friendship, Comment, Post, Profile, models
)

logger = logging.getLogger(__name__)


# VIEW 0 - AUTHENTICATION
class LoginRequiredMixin:
    """
    View mixin for requiring login.

    This mixin is used to require authentication for accessing views.
    Subclasses of this mixin will only allow access to authenticated users.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Dispatch method for requiring login.

        This method checks if the user is authenticated. If not, it redirects to the login page.

        Returns:
            HttpResponse: The response object.
        """
        return super().dispatch(*args, **kwargs)
# VIEW 1 - INDEX
class IndexView(TemplateView):
    """
    View for displaying the index page.

    This view renders the user_feed.html template as the index page.
    """
    template_name = 'user_feed.html'
# VIEW 2 - LOGIN
class LoginView(View):
    """
    View for handling user login.

    This view handles the GET and POST requests for user login.
    GET request: Renders the login.html template.
    POST request: Authenticates the user and logs them in if the credentials are valid.

    Attributes:
        template_name (str): The name of the template for the login page.
        success_url (str): The URL to redirect to after successful login.
    """

    template_name = 'login.html'
    success_url = 'user_feed'

    def get(self, request):
        """

        If the user is already authenticated, redirects to the success URL.
        Otherwise, renders the login.html template.

        Returns:
            HttpResponse: The response object.
        """
        if request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            return render(request, self.template_name)

    def post(self, request):
        """

        Authenticates the user using the provided credentials.
        If the credentials are valid, logs in the user and redirects to the success URL.
        If the credentials are invalid, displays an error message.

        Returns:
            HttpResponse: The response object.
        """
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
    """View for handling user logout.

    This view logs out the user and redirects to the login page.

    Attributes:
        url (str): The URL to redirect to after successful logout.
    """

    url = reverse_lazy('login')

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
# VIEW 4 - SIGNUP
class SignUpView(FormView):
    """
    View for user registration (signup).

    This view handles the user registration process.
    Renders the signup.html template for GET request.
    Validates and saves the registration form for POST request.

    Attributes:
        template_name (str): The name of the template for the signup page.
        form_class (Form): The form class for user registration.
        success_url (str): The URL to redirect to after successful signup.
    """

    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = 'user_feed'

    def form_valid(self, form):
        """Handle valid form submission.

        Saves the user registration form and logs in the user.
        Redirects to the success URL.

        Args:
            form (Form): The validated form object.

        Returns:
            HttpResponse: The response object.
        """
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """Handle invalid form submission.

        Renders the signup.html template with the invalid form.

        Args:
            form (Form): The invalid form object.

        Returns:
            HttpResponse: The response object.
        """
        return self.render_to_response(self.get_context_data(form=form))
# VIEW 5 - USER PROFILE - UPDATE PROFILE
class UserProfileFieldUpdateView(LoginRequiredMixin, View):
    """View for updating a user's profile field.

    This view allows a user to update their profile fields such as bio, gender, and profession.

    Attributes:
        model (Profile): The Profile model class.
    
    Methods:
        post(request, user_id): Handles the POST request for updating the profile field.

    """

    def post(self, request, user_id):
        """Handle the POST request for updating the profile field.

        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The ID of the user.

        Returns:
            JsonResponse: JSON response with the status of the update operation.

        """
        try:
            data = json.loads(request.body)

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
# VIEW 6 - USER PROFILE DETAILS
class UserProfileDetailsView(LoginRequiredMixin, DetailView):
    """

    This view displays the details of a user's profile.

    Attributes:
        model (Profile): The Profile model class.
        form_class (UpdateProfileForm): The form class for updating the profile.
        template_name (str): The name of the template for rendering the view.
        context_object_name (str): The name of the variable containing the user profile object in the template.
    
    Methods:
        get_object(queryset=None): Get the user profile object.
        get_context_data(**kwargs): Get the context data for rendering the template.

    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'user_profile_details.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        """
        Get the user profile object.

        Returns:
            Profile: The user's profile object.

        """
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            user = get_object_or_404(User, username=username)
            return user.profile
        else:
            return self.request.user.profile
        
    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.

        Returns:
            dict: The context data.

        """
        context = super().get_context_data(**kwargs)
  
        return context
# VIEW 7 - USER PROFILE (displays only the posts that the logged-in user has created)
class UserProfileView(LoginRequiredMixin, ListView):
    """

    This view displays a user's profile and the posts they have created.

    Attributes:
        template_name (str): The name of the template for rendering the view.
        context_object_name (str): The name of the variable containing the posts in the template.
        paginate_by (int): The number of posts to display per page.

    Methods:
        get_queryset(): Get the queryset for retrieving the user's posts.
        get_user_profile(): Get the user's profile object.
        get_context_data(**kwargs): Get the context data for rendering the template.
        post(request, *args, **kwargs): Handle the POST request.

    """
    template_name = 'user_profile.html'
    context_object_name = 'all_posts'
    paginate_by = 2

    def get_queryset(self):
        """
        Get the queryset for retrieving the user's posts.

        Returns:
            QuerySet: The queryset for retrieving the user's posts.

        """
        user_profile = self.get_user_profile()
        return Post.objects.filter(post_author=user_profile.user).order_by('-post_created_at')

    def get_user_profile(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            return user.profile
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.

        Returns:
            dict: The context data.

        """
        context = super().get_context_data(**kwargs)
        user_profile = self.get_user_profile()

        context['user_profile'] = user_profile
        context['all_post_comments'] = Comment.objects.all().order_by('-comment_created_at')
        context['post_form'] = PostForm()
        context['post_edit_form'] = PostEditForm()
        context['comment_form'] = CommentForm()
        context['is_profile_owner'] = user_profile.user == self.request.user
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
        """Handle the POST request.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.

        """
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
# VIEW 8 - USER FEED (displays posts of logged-in user and his friends)
class UserFeedView(LoginRequiredMixin, ListView):
    """View for displaying posts of the logged-in user and their friends."""
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
# VIEW 9 - USER SEARCH
class UserSearchView(LoginRequiredMixin, View):
    """View for searching for users."""
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
# VIEW 10 - USER DELETION & USER DELETION CONFIRMATION
class UserDeletionView(LoginRequiredMixin, TemplateView):
    """View for user deletion and user deletion confirmation."""
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
# VIEW 11 - FRIENDSHIP MANAGER
class FriendshipManager(View):
    """View for managing friend requests and friendships."""
    def send_friend_request(self, request, receiver_id):
        """Send a friend request to a user.

        Args:
            request (HttpRequest): The HTTP request object.
            receiver_id (int): The ID of the receiver user.

        Returns:
            HttpResponseRedirect: Redirects to the friend list view.

        Raises:
            HttpResponseBadRequest: If the receiver user does not exist.
        """
        try:
            receiver = User.objects.get(id=receiver_id)
            sender = request.user

            if receiver:

                friend_request = FriendRequest(sender=sender, receiver=receiver)
                friend_request.save()

                return redirect('friend_list')
            else:
                return HttpResponseBadRequest("Receiver does not exist")
        except User.DoesNotExist:
            return HttpResponseBadRequest("Receiver does not exist")
    def cancel_friend_request(self, request, request_id=None, **kwargs):
        """Cancel a friend request.

        Args:
            request (HttpRequest): The HTTP request object.
            request_id (int, optional): The ID of the friend request. Defaults to None.

        Returns:
            HttpResponseRedirect: Redirects to the friend list view.

        Raises:
            HttpResponseBadRequest: If the friend request does not exist or the request method is invalid.
        """
        if request.method == 'POST':
            try:
                friend_request = FriendRequest.objects.get(id=request_id)

                if friend_request.sender == request.user:
                    friend_request.cancel()

                    return redirect('friend_list')
                else:
                    return HttpResponseBadRequest("You are not the sender of this friend request.")
            except FriendRequest.DoesNotExist:
                return HttpResponseBadRequest("Friend request does not exist.")
        else:
            return HttpResponseBadRequest("Invalid request method")
    def reject_friend_request(self, request, request_id=None, **kwargs):
        """Reject a friend request.

        Args:
            request (HttpRequest): The HTTP request object.
            request_id (int, optional): The ID of the friend request. Defaults to None.

        Returns:
            HttpResponseRedirect: Redirects to the friend list view.

        Raises:
            HttpResponseBadRequest: If the friend request does not exist or the request method is invalid.
        """
        if request.method == 'POST':
            try:
                friend_request = FriendRequest.objects.get(id=request_id)

                if friend_request.receiver == request.user:
                    friend_request.delete()

                    return redirect('friend_list')
                else:
                    return HttpResponseBadRequest("You are not the receiver of this friend request.")
            except FriendRequest.DoesNotExist:
                return HttpResponseBadRequest("Friend request does not exist.")
        else:
            return HttpResponseBadRequest("Invalid request method")
    def accept_friend_request(self, request, request_id=None, **kwargs):
        """Accept a friend request.

        Args:
            request (HttpRequest): The HTTP request object.
            request_id (int, optional): The ID of the friend request. Defaults to None.

        Returns:
            HttpResponseRedirect: Redirects to the friend list view.

        Raises:
            HttpResponseBadRequest: If the friend request does not exist or the request method is invalid.
        """
        if request.method == 'POST':
            try:
                friend_request = FriendRequest.objects.get(id=request_id)

                if friend_request.receiver == request.user:
                    friend_request.accept()
    
                    Friendship.objects.create(sender=friend_request.sender, receiver=friend_request.receiver)

                    return redirect('friend_list')
                else:
                    return HttpResponseBadRequest("You are not the receiver of this friend request.")
            except FriendRequest.DoesNotExist:
                return HttpResponseBadRequest("Friend request does not exist.")
        else:
            return HttpResponseBadRequest("Invalid request method")
    def get_received_friend_requests(self, request, receiver_id):
        """Get the received friend requests for a user.

        Args:
            request (HttpRequest): The HTTP request object.
            receiver_id (int): The ID of the receiver user.

        Returns:
            QuerySet: Queryset of received friend requests.
        """
        received_friend_requests = FriendRequest.objects.filter(receiver_id=receiver_id)

        return received_friend_requests
    
    def get_sent_friend_requests(self, request):
        """Get the sent friend requests by a user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            QuerySet: Queryset of sent friend requests.
        """
        sent_friend_requests = FriendRequest.objects.filter(sender=request.user)
       
        return sent_friend_requests

    def get_existing_friendships(self, request):
        """Get the existing friendships for a user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            QuerySet: Queryset of existing friendships.
        """
        
        existing_friendships = Friendship.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        
        return existing_friendships


    def remove_friendship(self, request, friendship_id=None):
        """Remove a friendship.

        Args:
            request (HttpRequest): The HTTP request object.
            friendship_id (int, optional): The ID of the friendship. Defaults to None.

        Returns:
            HttpResponseRedirect: Redirects to the friend list view.

        Raises:
            HttpResponseBadRequest: If the friendship does not exist.
        """
        try:
            friendship = Friendship.objects.get(id=friendship_id)

            if friendship.sender == request.user or friendship.receiver == request.user:
                friendship.delete()

                return redirect('friend_list')
            else:
                return HttpResponseBadRequest("You are not part of this friendship.")
        except Friendship.DoesNotExist:
            return HttpResponseBadRequest("Friendship does not exist.")

    
    def get(self, request):
        """Handle the GET request for the friend list view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
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
        """Handle the POST request for the friend list view.

        Args:
            request (HttpRequest): The HTTP request object.
            kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
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
# VIEW 12 - UPLOAD IMAGE AND PROFILE BANNER
class UploadProfileImageView(LoginRequiredMixin, FormView):
    """View for uploading user profile image and banner."""
    template_name = 'user_profile_image.html'
    form_class = UploadProfileImageForm

    def get_form_kwargs(self):
        """Get the keyword arguments for initializing the form."""
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
# VIEW 13 - POST CREATE
class PostCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new post."""
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        profile = self.request.user.profile
        form.instance.post_author_image = profile.profile_image
        form.instance.post_author = self.request.user
        return super().form_valid(form)
# VIEW 14 - POST LIST
class PostListView(ListView):
    """View for listing posts."""
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list_context'
# VIEW 15 - POST DETAILS
class PostDetailsView(DetailView):
    """View for displaying details of a post."""
    model = Post
    template_name = 'post_edit_page.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        """Handle GET request and render the post edit page."""
        self.object = self.get_object()
        if not self.is_friend(request.user, self.object.post_author):
            return HttpResponseForbidden("You are not authorized to view this post.")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def is_friend(self, user, author):
        """Check if the given user is a friend of the post author."""
        if user == author:
            return True  
        return Friendship.objects.filter(
            (Q(sender=user, receiver=author) | Q(sender=author, receiver=user)),
            status='accepted'
        ).exists()

    def get_context_data(self, **kwargs):
        """Get the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        context['is_post_edit_page'] = True
        context['all_posts'] = Post.objects.all().order_by('-post_created_at')
        context['all_post_comments'] = Comment.objects.all().order_by('-comment_created_at')
      
        return context
# VIEW 16 - POST EDIT PAGE
class PostEditView(UpdateView):
    """View for editing a post."""
    model = Post
    form_class = PostEditForm
    template_name = 'post_edit_page.html'
    context_object_name = 'post'
    success_url = reverse_lazy('user_feed')
      
    def get_form_kwargs(self):
        """Get the keyword arguments for initializing the form."""
        kwargs = super().get_form_kwargs()
        post = Post.objects.get(pk=self.kwargs['pk'])
        kwargs['instance'] = post
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)
        post_content = form.cleaned_data['post_content']
        post.post_content = post_content 
        post.save()
        
        return redirect('user_feed')

    def get_context_data(self, **kwargs):
        """Get the context data for rendering the post edit page."""
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all() 
        return context
# VIEW 17 - POST LIKE
class PostLikeToggleView(LoginRequiredMixin, View):
    """View for toggling the like status of a post."""
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
# VIEW 18 - POST DELETE
class PostDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a post."""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('user_feed')
# VIEW 19 - COMMENT CREATE
class CommentCreateView(LoginRequiredMixin, CreateView):
    """View for creating a comment on a post."""
    model = Comment
    form_class = CommentForm
    template_name = 'post_comment_create.html'  
    success_url = reverse_lazy('user_feed')

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.comment_on_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        super().form_valid(form)
        return redirect('user_feed')
# VIEW 20 - PASSWORD RESET 
class PasswordResetView(View):
    """View for resetting the password."""
    template_name = 'password_reset_page.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('login')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 != new_password2:

                return self.form_invalid(form)

            username = form.cleaned_data['username']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:

                return self.form_invalid(form)

            user.set_password(new_password1)
            user.save()

            profile = user.profile
            profile.user.set_password(new_password1)
            profile.user.save()

            return redirect(self.success_url)

        return self.form_invalid(form)

    def get(self, request):
        """Handle the GET request to render the password reset page."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
