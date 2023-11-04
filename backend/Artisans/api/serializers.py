from rest_framework import serializers

from django.contrib.auth.models import Group
from Artisans.models import User, Profile, Category, Artisan, JobRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['username', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile

        fields = ['user', 'phone_number', 'location', 'profile_picture_url', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        fields = ['name', 'description']

class ArtisansSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Artisan

        fields = ['user', 'categories', 'bio', 'experience', 'location', 'whatsapp', 'tel']

class JobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest

        fields = ['client', 'artisan', 'title', 'description', 'status']

    