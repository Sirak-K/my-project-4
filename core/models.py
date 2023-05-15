# File: models.py
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.db.models.signals import post_save


# MODEL 1 - PROFILE
class Profile(models.Model):
    date_of_birth = models.DateField(auto_now=False, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True) 
    bio = models.TextField(blank=True, null=True)
   

    PROFESSION_CHOICES = (
        ('O', 'Student'),
        ('M', 'Working'),
        ('F', 'Not Working'),
        ('T', 'Other'),
        ('N', 'None selected'),
    )
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES, default="N", blank=True, null=True)

    GENDER_CHOICES = (
        ('O', 'Other'),
        ('M', 'He/Him'),
        ('F', 'She/Her'),
        ('T', 'They/Them'),
        ('N', 'None selected'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    

    def get_user_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return f"{self.user.username}'s Profile"

# DECORATOR - PROFILE: CREATE
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# MODEL 2 - POST
class Post(models.Model):
    post_title = models.CharField(max_length=50, default='')
    post_content = models.TextField(max_length=200, default='')
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def time_since_posted(self):
        now = timezone.now()
        time_difference = now - self.post_created_at
        if time_difference.seconds < 60:
            return "Just now"
        return f"{timesince(self.post_created_at)} ago"

    def get_post_author_name(self):
            return self.post_author.get_full_name()

    def __str__(self):
        return f'Post {self.pk} by {self.post_author}'
    
    def save(self, *args, **kwargs):
        print('Post save called')
        super().save(*args, **kwargs)
 
# MODEL 3 - COMMENT
class Comment(models.Model):
    comment_for_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_on_post')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    comment_content = models.TextField(max_length=300, blank=False)
    comment_created_at = models.DateTimeField(default=timezone.now)

    def time_since_posted(self):
        now = timezone.now()
        time_difference = now - self.comment_created_at
        if time_difference.seconds < 60:
            return "Just now"
        return f"{timesince(self.comment_created_at)} ago"


    def __str__(self):
        return f'Comment {self.pk} by {self.comment_author}'





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
