from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Comment, Post, Profile,
    FriendRequest, Friendship
)


class CustomUserCreationForm(UserCreationForm):
    """Custom form for user creation.

    Inherits from UserCreationForm and adds additional fields.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
class CustomPasswordResetForm(forms.Form):
    """Custom form for password reset.

    Validates new passwords and checks the validity of the username.
    """
    username = forms.CharField(label='Enter Username')
    new_password1 = forms.CharField(label='Enter New Password')
    new_password2 = forms.CharField(label='Enter Confirm New Password')

    def clean(self):
        """Custom cleaning method for password reset form.

        Validates new passwords and checks the validity of the username.
        """
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        username = cleaned_data.get('username')

        print("Executing clean method")  # Debugging statement

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('New passwords do not match.')

        if username and not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Invalid username.')

        print("Clean method executed successfully")  # Debugging statement

        return cleaned_data
class UserSearchForm(forms.Form):
    """Form for user search.

    Allows users to search for other users.
    """
    search_query = forms.CharField(max_length=100)
class UpdateProfileForm(forms.ModelForm):
    """Form for updating user profile.

    Uses the Profile model and allows users to update their bio, gender, and profession.
    """
    class Meta:
        model = Profile
        fields = ['bio', 'gender', 'profession', ]
class UploadProfileImageForm(forms.ModelForm):
    """Form for uploading profile images.

    Allows users to update their profile image and banner image.
    """
    class Meta:
        model = Profile
        fields = ['profile_image', 'banner_image']
        labels = {
            'profile_image': 'Update Profile Image',
            'banner_image': 'Update Profile Banner',
        }
class PostForm(forms.ModelForm):
    """Form for creating a post.

    Uses the Post model and allows users to create a post with a title and content.
    """
    class Meta:
        model = Post
        fields = ['post_title', 'post_content']
        widgets = {
            'post_content': forms.Textarea(attrs={'class': 'post-content'}),
        }
        labels = {
            'post_title': 'Post Title',
            'post_content': 'Post Content'
        }
        help_texts = {
            'post_title': 'Maximum 50 characters',
            'post_content': 'Maximum 200 characters'
        }
        error_messages = {
            'post_title': {
                'max_length': 'The post title cannot exceed 50 characters.'
            },
            'post_content': {
                'max_length': 'The post content cannot exceed 200 characters.'
            }
        }

    def clean_post_title(self):
        """Custom cleaning method for post title.

        Validates the length of the post title.
        """
        post_title = self.cleaned_data['post_title']
        if len(post_title) > 50:
            raise forms.ValidationError("The post title cannot exceed 50 characters.")
        return post_title

    def clean_post_content(self):
        """Custom cleaning method for post content.

        Validates the length of the post content.
        """
        post_content = self.cleaned_data['post_content']
        if len(post_content) > 200:
            raise forms.ValidationError("The post content cannot exceed 200 characters.")
        return post_content
class PostEditForm(forms.ModelForm):
    """Form for editing a post.

    Uses the Post model and allows users to edit the post content.
    """
    class Meta:
        model = Post
        fields = ['post_content']
        widgets = {
            'post_content': forms.Textarea(attrs={'class': 'post-content'}),
        }
class CommentForm(forms.ModelForm):
    """Form for adding comments to a post.

    Uses the Comment model and allows users to add comments to a post.
    """
    class Meta:
        model = Comment
        fields = ['comment_content']
class FriendRequestForm(forms.ModelForm):
    """Form for sending friend requests.

    Uses the FriendRequest model and allows users to send friend requests to other users.
    """
    class Meta:
        model = FriendRequest
        fields = ['receiver']

    def clean(self):
        """Custom cleaning method for friend request form.

        Validates the receiver field and checks the relationship and dependencies.
        """
        cleaned_data = super().clean()
        receiver = cleaned_data.get('receiver')
        sender = self.instance.sender

        # Mandatory Fields and Basic Data Validation
        # Check if the receiver field is empty
        if not receiver:
            raise forms.ValidationError("Receiver field is required.")

        # Relationship and Dependency Validation
        # Check if the sender and receiver are the same
        if sender and sender == receiver:
            raise forms.ValidationError("Sender cannot accept their own friend request.")

        # Check if the sender and receiver are already friends
        if sender and receiver:
            if Friendship.objects.filter(sender=sender, receiver=receiver).exists():
                raise forms.ValidationError("You are already friends with this user.")

        return cleaned_data
