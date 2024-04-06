from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post, React, Comment

class Task(models.Model):
    title = models.CharField(max_length=100, default='New task')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_due = models.DateField()
    date_created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.user} task ({self.id})'

class Notification(models.Model):
    NOTIFICATION_TYPE = [
        ('System-feature', 'System notification - New feature'),
        ('System-news', 'System notification - Admin news'),
        ('Blog-react', 'Blog notification - React'),
        ('Blog-comment', 'Blog notification - Comment'),
        ('Blog-share', 'Blog notification - Share'),
        ('User-friend', 'User notification - Friends'),
        ('User-task', 'User notification - Task overdue'),
        ('Other', 'Other notification')
    ]
    
    REACTION_CHOICES = [
        ('Like', 'Like'),
        ('Love', 'Love'),
        ('Haha', 'Haha'),
        ('Wow', 'Wow'),
        ('Sad', 'Sad'),
        ('Angry', 'Angry')
    ]

    sending_user = models.ForeignKey(User, related_name='sent_notifications', null=True, blank=True, on_delete=models.SET_NULL)
    receiving_user = models.ForeignKey(User, related_name='received_notifications', null=True, blank=True, on_delete=models.SET_NULL)
    notification_type = models.CharField(blank=False, null=False, choices=NOTIFICATION_TYPE, max_length=20, default='Other')
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)
    reaction = models.CharField(max_length=6, choices=REACTION_CHOICES, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.sending_user} sends to {self.receiving_user} a notification in type of {self.notification_type}'




