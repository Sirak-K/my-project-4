# File: views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import DeleteView, CreateView, ListView, DetailView
from .forms import PostForm, PostEditForm, UpdateProfileForm, UpdateProfileImageForm
from .models import Post, Profile 


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
    return redirect('login_view')

# VIEW 4 - HOME [ LOGGED-IN ] --------->
@login_required
def index(request):
   
    return render(request, 'user_feed.html')

# VIEW 5 - USER FEED (displays created posts)
def user_feed(request):
    get_all_posts = Post.objects.all().order_by('-post_created_at')  # Reverse the order by using '-post_created_at'
    return render(request, 'user_feed.html', {'all_posts': get_all_posts})

# VIEW 6 - LOGGED-IN - PROFILE
@login_required
def user_profile(request):
    get_all_posts = Post.objects.all().order_by('-post_created_at')  # Reverse the order by using '-post_created_at' 
    user_profile = request.user.profile


    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')
    else:
        form = UpdateProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'form': form,
        'all_posts': get_all_posts
    }
    return render(request, 'user_profile.html', context)
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


# VIEW 9 - Post List
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list_context'
# VIEW 10 - Post Details
class PostDetailsView(DetailView):
    model = Post
    template_name = 'post_details_page.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details', pk=post.pk)
        else:
            # Handle form errors if needed
            return self.get(request, *args, **kwargs)  # Render the form again with errors

# VIEW 11 - Post Create
class PostCreateView(CreateView):
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



# VIEW 12 - Post Delete
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = 'user_feed'


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




