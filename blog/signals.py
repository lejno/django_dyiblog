from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile whenever a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def ensure_user_profile_exists(sender, instance, **kwargs):
    """Ensure a UserProfile exists after user save (for edge cases)."""
    try:
        # Accessing instance.profile will raise UserProfile.DoesNotExist if missing
        _ = instance.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
