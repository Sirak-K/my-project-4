from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
# Format Example:

# Field type: ForeignKey
# Related model: User
# on_delete: CASCADE

    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    

    def __str__(self):
        return self.user.username
