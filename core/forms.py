from django import forms
from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'privacy_settings']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UpdateProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'banner_image']