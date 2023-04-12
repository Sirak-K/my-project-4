from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


# MODEL 1 - PROFILE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # One-to-one relationship with User
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    privacy_settings = models.CharField(max_length=30, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    # website = models.URLField(blank=True)
    # phone_number = models.CharField(max_length=20, blank=True)
    # gender = models.CharField(choices=GENDER_CHOICES, max_length=2, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
# DECOR 2 - PROFILE: CREATE
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# MODEL 3 - POST
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key relationship with User
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    privacy_settings = models.CharField(max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the post is created
    def time_since_posted(self):
        now = timezone.now()
        time_difference = now - self.timestamp
        if time_difference.seconds < 60:
            return "Just now"
        return f"{timesince(self.timestamp)} ago"

    def count_likes(self):
        return self.likes.count()

    def count_comments(self):
        return self.comments.count()
    
    def __str__(self):
        return f"{self.author.username}'s Post"
# MODEL 4 - COMMENT
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author.username}'s comment on {self.post}"
# MODEL 5 - LIKE
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} liked {self.post.author.username}'s Post"
# MODEL 6 - FRIEND REQUEST
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    status = models.CharField(max_length=20)  # "Pending", "Accepted", "Rejected"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} sent a friend request to {self.recipient.username}"
# MODEL 7 - FRIEND LIST
class FriendList(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_lists_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_lists_user2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username} are friends"
# MODEL 8 - NOTIFICATION
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)  # "friend_request", "like", "comment", etc.
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Set to False by default
    def __str__(self):
        return f"{self.user.username}'s {self.type} Notification"
# MODEL 9 - PRIVATE MESSAGES 
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender.username} sent a message to {self.recipient.username}"
# MODEL 10 - GROUP
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} Group"
# MODEL 11 - GROUP MEMBERS
class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} is a member of {self.group.name}"
# MODEL 12 - GROUP POSTS
class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='group_posts/', blank=True, null=True)
    video = models.FileField(upload_to='group_videos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author.username}'s Post in {self.group.name} Group"
    

