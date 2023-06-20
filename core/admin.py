from django.contrib import admin
from .models import FriendRequest, Friendship, Comment, Post, Profile


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friendship)
admin.site.register(FriendRequest)