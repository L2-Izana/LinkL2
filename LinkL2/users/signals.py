from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Avatar
from sidebar.models import Notification

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=User)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(sending_user=User.objects.get(username='LucasDo'), receiving_user=instance, content='Welcome to LinkL2. Enjoy your experience here!', notification_type='System-news')

@receiver(post_save, sender=Profile)
def create_avatar(sender, instance, created, **kwargs):
    if created:
        Avatar.objects.create(profile=instance)

@receiver(post_save, sender=Profile)
def save_avatar(sender, instance, **kwargs):
    instance.avatar.save()