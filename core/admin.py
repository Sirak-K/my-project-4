# File: admin.py
from django.contrib import admin
from .models import Post, Profile


admin.site.register(Profile)
admin.site.register(Post)


