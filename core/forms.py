# File: forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Comment, Post, Profile, FriendRequest, Friendship

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
                'post_title', 
                'post_content', 
                  ]
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content',
                  'post_title',
                  ]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['receiver']

    def clean(self):
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

class UserSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'gender', 'profession', ]
class UpdateProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'banner_image' ]
