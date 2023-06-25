from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timesince, timezone
from cloudinary.models import CloudinaryField

# MODEL 1 - PROFILE
class Profile(models.Model):
    """
    Represents a user profile associated with a Django User.

    Attributes:
        user (User): The User instance associated with this profile.
        date_of_birth (date): The date of birth of the user.
        profile_image (ImageField): The user's profile image.
        banner_image (ImageField): The banner image displayed on the user's profile.
        bio (str): The user's biography.

    Choices:
        PROFESSION_CHOICES (tuple): Choices for the user's profession.
        GENDER_CHOICES (tuple): Choices for the user's gender.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    date_of_birth = models.DateField(auto_now=False, blank=True, null=True)
    profile_image = CloudinaryField('profile_images', blank=True, null=True)
    banner_image = CloudinaryField('banner_images', blank=True, null=True)
    bio = models.TextField(default='', blank=True, null=True)

    PROFESSION_CHOICES = (
        ('O', 'Student'),
        ('M', 'Working'),
        ('F', 'Not Working'),
        ('T', 'Other'),
        ('N', 'None selected'),
    )
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES, default="N")

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

    def get_friends(self):
        """
        Get a list of friends associated with this profile.

        Returns:
            list: A list of User instances representing the friends.
        """
        user = self.user
        friends = Friendship.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user),
            status='accepted'
        )
        return [friend.sender if friend.sender != user else friend.receiver for friend in friends]

    def __str__(self):
        return f"{self.user.username}'s Profile" 
# DECORATOR
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# MODEL 2 - POST
class Post(models.Model):
    """
    Represents a post created by a user.

    Attributes:
        post_author (User): The author of the post.
        post_title (str): The title of the post.
        post_content (str): The content of the post.
        post_created_at (datetime): The timestamp when the post was created.
        post_likes (QuerySet): A many-to-many relationship representing the users who liked the post.
        post_comments (QuerySet): A many-to-many relationship representing the comments on the post.
    """

    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=50)
    post_content = models.TextField(max_length=200)
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    post_comments = models.ManyToManyField('Comment', related_name='commented_posts')

    def post_likes_count(self):
        """
        Get the number of likes on the post.

        Returns:
            int: The count of likes on the post.
        """
        return self.post_likes.count()

    def is_liked_by_user(self, user):
        """
        Check if the post is liked by a specific user.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has liked the post, False otherwise.
        """
        return self.post_likes.filter(id=user.id).exists()

    def time_since_posted(self):
        """
        Get the time since the post was created.

        Returns:
            str: A human-readable representation of the time elapsed since the post was created.
        """
        now = timezone.now()
        time_difference = now - self.post_created_at
        if time_difference.seconds < 60:
            return "Just now"
        return f"{timesince(self.post_created_at)} ago"

    def get_post_author_name(self):
        return self.post_author.get_full_name()
    
    @property
    def author_profile_image(self):
        """
        Get the URL of the author's profile image.

        Returns:
            str: The URL of the author's profile image.
        """
        if self.post_author.profile.profile_image:
            return self.post_author.profile.profile_image.url
        else:
            return '/static/img/default_profile_image.png'

    def __str__(self):
        return f'Post {self.pk} by {self.post_author}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
# MODEL 3 - COMMENT
class Comment(models.Model):
    """
    Represents a comment made by a user on a post.

    Attributes:
        comment_on_post (Post): The post that this comment belongs to.
        comment_created_at (datetime): The timestamp when the comment was created.
        comment_author (User): The user who authored the comment.
        comment_content (str): The content of the comment.
    """

    comment_on_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments_for_post")
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField(max_length=100)

    def get_comment_author_name(self):
        return self.comment_author.get_full_name()
    
    @property
    def author_profile_image(self):
        """
        Get the URL of the profile image of the comment author.

        Returns:
            str: The URL of the comment author's profile image.
        """
        if self.comment_author.profile.profile_image:
            return self.comment_author.profile.profile_image.url
        else:
            return '/static/img/default_profile_image.png'

    def __str__(self):
        return f'Comment {self.pk} by {self.comment_author}'
# MODEL 4 - Friendship
class Friendship(models.Model):
    """
    Represents a friendship between two users.

    Attributes:
        STATUS_CHOICES (tuple): Choices for the status of the friendship.
        sender (User): The user who initiated the friendship.
        receiver (User): The user who received the friendship request.
        status (str): The status of the friendship.
    """

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_friendships', null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friendships', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='accepted')

    def __str__(self):
        sender_full_name = self.sender.profile.get_user_name() if self.sender else "None"
        receiver_full_name = self.receiver.profile.get_user_name() if self.receiver else "None"
        return f"{sender_full_name} and {receiver_full_name}"
# MODEL 5 - FriendRequest
class FriendRequest(models.Model):
    """
    Represents a friend request between two users.

    Attributes:
        sender (User): The user who sent the friend request.
        receiver (User): The user who received the friend request.
        status (str): The status of the friend request.

    Methods:
        accept: Accept the friend request.
        reject: Reject the friend request.
        cancel: Cancel the friend request.
        __str__: Get a string representation of the friend request.
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests', null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests', null=True)
    status = models.CharField(max_length=10, choices=Friendship.STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ['sender', 'receiver']

    def accept(self):
        """
        Accept the friend request.

        If the friend request status is 'pending', it will be accepted and the status will be updated to 'accepted'.
        After accepting the request, the friend request will be deleted.

        Returns:
            None
        """
        if self.status != 'pending':
            return

        self.status = 'accepted'
        print("Friend Request ACCEPTED.")
        self.save()

        self.delete()
        print("Friend Request DELETED.")
        
    def reject(self):
        """
        Reject the friend request.

        If the friend request status is 'pending', it will be rejected and the status will be updated to 'rejected'.

        Returns:
            None
        """
        if self.status != 'pending':
            return

        self.status = 'rejected'
        self.save()

    def cancel(self):
        """
        Cancel the friend request.

        If the friend request status is 'pending', it will be deleted.

        Returns:
            None
        """
        if self.status == 'pending':
            self.delete()

    def __str__(self):
        return f"Friend request from {self.sender.username} to {self.receiver.username}"
    
