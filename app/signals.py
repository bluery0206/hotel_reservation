
from django.db.models.signals import post_save # Signal when something is saved
from django.contrib.auth.models import User # Default user model
from django.dispatch import receiver # Connects signals to functions

from .models import Profile # Your Profile model

# Rule 1: When a User is saved, run this
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created: # Only for new users (not updates)
        Profile.objects.create(user=instance) # Make their profile

# Rule 2: When a User is saved AGAIN, save their profile too
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() # Update profile if user changes