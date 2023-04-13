from django.contrib import admin
from .models import Comment, Like, Post, Profile, FriendList, FriendRequest


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(FriendList)
admin.site.register(FriendRequest)

