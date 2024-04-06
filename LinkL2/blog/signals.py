from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, PostImage


@receiver(post_save, sender=Post)
def create_profile(sender, instance, created, **kwargs):
    if created:
        PostImage.objects.create(post=instance)

@receiver(post_save, sender=Post)
def save_profile(sender, instance, **kwargs):
    instance.postimage.save()