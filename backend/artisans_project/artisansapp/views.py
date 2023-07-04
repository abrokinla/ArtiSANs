from rest_framework import generics
from .models import User, Profile, Category, Artisan, JobRequest
from .serializers import UserSerializer, ProfileSerializer, CategorySerializer, ArtisanSerializer, JobRequestSerializer
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.db import transaction

# Create your views here.

# Create user view
class ClientUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Separate the data for User and Profile
        user_data = request.data.get('user', {})
        profile_data = request.data.get('profile', {})

        # Create the User instance
        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        try:
            # Create the Profile instance
            profile_data['user'] = user.id
            profile_serializer = ProfileSerializer(data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                profile_serializer.save()

        except Exception as e:
            # Rollback user creation if profile creation fails
            user.delete()
            raise e

        return JsonResponse({
            'success': True,
            'data': user_serializer.data
        }, status=201)