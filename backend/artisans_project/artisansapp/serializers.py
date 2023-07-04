from rest_framework import serializers
from .models import User, Profile, Category, Artisan, JobRequest


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'phone_number', 'location', 'profile_picture_url', 'bio']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'profile']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArtisanSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Artisan
        fields = '__all__'


class JobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest
        fields = '__all__'
