# File: views.py
from django.views.generic import CreateView, ListView, DetailView
from .forms import PostForm, CommentForm, UpdateProfileForm, UpdateProfileImageForm
from .models import Comment, Post, Profile, FriendRequest, FriendList
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# VIEW - SIGN-UP
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
# VIEW - LOG-IN
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
# ---------> VIEW [ LOG-OUT ] --------->
def logout_view(request):
    logout(request)
    return redirect('login_view')

# VIEW 3 - HOME [ LOGGED-IN ] --------->
@login_required
def index(request):
   
    return render(request, 'user_feed.html')

# VIEW 4 - USER FEED (displays created posts)
def user_feed(request):
    get_all_posts = Post.objects.all()  
    return render(request, 'user_feed.html', {'all_posts': get_all_posts})


# VIEW - Post List
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list_context'

# VIEW - Post Details
class PostDetailsView(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post_details_context'



class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = '/user_feed/'

    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super().form_valid(form)


@require_POST
@login_required
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.post_author == request.user:
        post.delete()
        return redirect('post_list')
    else:
        return HttpResponseForbidden()


# VIEW - LOGGED-IN - PROFILE
@login_required
def user_profile(request):
    get_all_posts = Post.objects.all()  
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

# VIEW- LOGGED-IN - PROFILE - UPLOAD IMAGES
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




# VIEW - LOGGED-IN - PROFILE - UPDATE PROFILE DETAILS
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












