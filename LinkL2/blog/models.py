from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True, blank=True, upload_to='post_pics')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": self.id})
    

class React(models.Model):
    REACTION_CHOICES = [
        ('Like', 'Like'),
        ('Love', 'Love'),
        ('Haha', 'Haha'),
        ('Wow', 'Wow'),
        ('Sad', 'Sad'),
        ('Angry', 'Angry')
    ]
    reaction = models.CharField(max_length=6, choices=REACTION_CHOICES, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.first_name + " " + self.user.last_name} reacted with {self.reaction} to {self.post.author.first_name + " " + self.post.author.last_name}\'s {self.post.title}'    
    
class Comment(models.Model):
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.user.profile.name} commented to {self.post.title}: {self.comment}'