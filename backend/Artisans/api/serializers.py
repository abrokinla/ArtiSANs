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

        fields = ['__all__']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        fields = ['__all__']

class ArtisansSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Artisan

        fields = ['__all__']

class JobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest

        fields = ['__all__']

    