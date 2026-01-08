from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import StaffProfile

@receiver(post_save, sender=User)
def ensure_staff_profile(sender, instance: User, created: bool, **kwargs):
    if instance.role == User.Role.STAFF:
        StaffProfile.objects.get_or_create(user=instance)
