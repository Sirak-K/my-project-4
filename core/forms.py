# File: forms.py
from django import forms
from .models import Comment, Post, Profile

# JANI FIELDS TO BE INPUTTED I EN FORM


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
     


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'gender', 'profession', ]

class UpdateProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'banner_image' ]

