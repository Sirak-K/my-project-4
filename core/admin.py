from django.contrib import admin
from .models import Post, Profile, FriendRequest, Notification, Group, GroupMember, Message


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Message)
