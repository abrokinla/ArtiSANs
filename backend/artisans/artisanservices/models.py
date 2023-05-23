from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('artisan', 'Artisan'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    # Add any additional fields or customization to the User model here

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    profile_picture_url = models.URLField()
    bio = models.TextField()

    # Add any additional fields and methods as needed

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Artisan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    # Add artisan-specific fields and methods

    def __str__(self):
        return self.user.username

class JobRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')

    # Add any additional fields and methods

    def __str__(self):
        return self.title

