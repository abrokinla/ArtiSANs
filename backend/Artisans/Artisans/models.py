from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
class User(AbstractUser):
    app_label = 'Artisans'
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('artisan', 'Artisan'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    # Add any additional fields or customization to the User model here

    # Add related_name to the groups field
    groups = models.ManyToManyField(Group, related_name='custom_user_set')

    # Add related_name to the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        verbose_name='user permissions',
        blank=True,
    )

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
    description = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name

class Artisan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    # Add artisan-specific fields and methods
    bio = models.TextField(default='')
    experience = models.TextField(default='')
    location = models.TextField(default='')
    whatsapp = models.CharField(max_length=20, default=None, null=True, blank=True)
    tel = models.CharField(max_length=20, default=None, null=True, blank=True)

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

