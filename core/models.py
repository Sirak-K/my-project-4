# File: models.py

from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils import timesince


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
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES, default="N", blank=True)

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
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=50)
    post_content = models.TextField(max_length=200)
    post_likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    post_comments = models.ManyToManyField('Comment', related_name='commented_posts')



    def post_likes_count(self):
        return self.post_likes.count()

    def is_liked_by_user(self, user):
        return self.post_likes.filter(id=user.id).exists()

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

    comment_on_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments_for_post")
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField(max_length=100)


    def get_comment_author_name(self):
        return self.comment_author.get_full_name()

    def __str__(self):


        return f'Comment {self.pk} by {self.comment_author}'



# File: models.py



# MODEL 4 - Friendship
class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='initiated_friendships', null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_friendships', null=True)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='accepted')

    def __str__(self):
        sender_full_name = self.sender.profile.get_user_name() if self.sender else "None"
        receiver_full_name = self.receiver.profile.get_user_name() if self.receiver else "None"
        return f"Friendship between {sender_full_name} and {receiver_full_name}"

# MODEL 5 - FriendRequest
class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_friend_requests', null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_friend_requests', null=True)
    status = models.CharField(max_length=10, choices=Friendship.STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ['sender', 'receiver']

    def accept(self):
        if self.status != 'pending':
            return

        self.status = 'accepted'
        print("Friend Request ACCEPTED.")
        self.save()

        self.delete()
        print("Friend Request DELETED.")
        
    def reject(self):
        if self.status != 'pending':
            return

        self.status = 'rejected'
        self.save()

    def cancel(self):
        if self.status == 'pending':
            self.delete()

    def __str__(self):
        return f"Friend request from {self.sender.username} to {self.receiver.username}"
    








    