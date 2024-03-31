from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(blank=False, null=False, max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M')
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    curr_work = models.CharField(blank=True, null=True, max_length=100, verbose_name='Current work')
    highest_education = models.CharField(blank=True, null=True, max_length=100)
    curr_place = models.CharField(blank=True, null=True, max_length=100, verbose_name='Living place')
    phone_contact = models.CharField(blank=True, null=True, max_length=100)
    social_link = models.CharField(blank=True, null=True, max_length=100)
    relationship = models.CharField(blank=True, null=True, max_length=10, choices=[('Single', 'Single'), ('Dating', 'Dating'), ('Married', 'Married'), ('Private', 'Private')])
    name = models.CharField(blank=False, null=True, max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def set_image_based_on_sex(self):
        if not self.image or self.image.name == 'default.jpg':
            if self.sex == 'M':
                self.image = 'male.jpg'
            elif self.sex == 'F':
                self.image = 'female.jpg'

    def save_name(self):
        self.name = self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):
        self.set_image_based_on_sex()
        self.save_name()

        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

