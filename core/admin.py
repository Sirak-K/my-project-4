# File: admin.py
from django.contrib import admin
from .models import Friendship, Comment, Post, Profile


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friendship)


