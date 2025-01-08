from accounts.models import UserProfile
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_post_save(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print(f"User profile Created for user {instance.username}")
        instance.save()