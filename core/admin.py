from django.contrib import admin
from .models import GroupPost, Comment, Like, Post, Profile, FriendList, FriendRequest, Notification, Group, GroupMember, Message


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FriendList)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupPost)
