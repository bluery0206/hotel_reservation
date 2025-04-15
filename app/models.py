from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Profile(models.Model):
    """ Profile """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    image = ResizedImageField(
        size = [100, 150],
        crop = ['middle', 'center'],
        upload_to = 'profile_images',
        blank = True,
        null = True,
        default = "default.png",
    )
