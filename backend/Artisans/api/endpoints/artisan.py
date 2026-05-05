from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from Artisans.models import Artisan, Category, Profile
from api.serializers import ArtisanSerializer, CategorySerializer, UserSerializer, ArtisanUpdateSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    """Handle user registration and JWT authentication"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Refresh to get profile data
            user.refresh_from_db()
            
            # If registering as artisan, create artisan profile
            if user.role == 'artisan':
                Artisan.objects.create(user=user)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'phone_number': user.profile.phone_number,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ArtisanViewSet(viewsets.ModelViewSet):
    queryset = Artisan.objects.filter(is_available=True)
    serializer_class = ArtisanSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def list_all(self, request):
        """List all available artisans with optional filters"""
        queryset = self.get_queryset()
        category = request.query_params.get('category')
        location = request.query_params.get('location')
        min_rating = request.query_params.get('min_rating')
        
        if category:
            queryset = queryset.filter(categories__name__icontains=category)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_rating:
            # Filter by average rating (this is a simplified version)
            queryset = queryset.filter(reviews_received__rating__gte=min_rating)
        
        serializer = self.get_serializer(queryset.distinct(), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get full artisan profile including reviews"""
        artisan = get_object_or_404(Artisan, pk=pk)
        from .serializers import ReviewSerializer
        data = self.get_serializer(artisan).data
        data['reviews'] = ReviewSerializer(artisan.reviews_received.all(), many=True).data
        return Response(data)
    
    @action(detail=False, methods=['post'])
    def verify_nin(self, request):
        """Submit NIN for verification (mock for MVP)"""
        user = request.user
        nin = request.data.get('nin')
        if not nin or len(nin) != 11:
            return Response({'error': 'Valid 11-digit NIN required'}, status=status.HTTP_400_BAD_REQUEST)
        user.nin_number = nin
        user.nin_verified = True  # Mock verification for MVP
        user.save()
        return Response({'message': 'NIN verified successfully'})
    
    @action(detail=False, methods=['post'])
    def verify_bvn(self, request):
        """Submit BVN for verification (mock for MVP)"""
        user = request.user
        bvn = request.data.get('bvn')
        if not bvn or len(bvn) != 11:
            return Response({'error': 'Valid 11-digit BVN required'}, status=status.HTTP_400_BAD_REQUEST)
        user.bvn_number = bvn
        user.bvn_verified = True  # Mock verification for MVP
        user.save()
        return Response({'message': 'BVN verified successfully'})
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's artisan profile"""
        try:
            artisan = Artisan.objects.get(user=request.user)
        except Artisan.DoesNotExist:
            return Response({'error': 'Artisan profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method in ['PUT', 'PATCH']:
            from api.serializers import ArtisanUpdateSerializer
            serializer = ArtisanUpdateSerializer(artisan, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Return full artisan data after update
                return Response(self.get_serializer(artisan).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(self.get_serializer(artisan).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def list_with_artisans(self, request):
        """List categories with artisan count"""
        categories = Category.objects.all()
        data = []
        for cat in categories:
            data.append({
                'id': cat.id,
                'name': cat.name,
                'description': cat.description,
                'artisan_count': cat.artisan_set.filter(is_available=True).count()
            })
        return Response(data)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def artisan_me_view(request):
    """Get or update current user's artisan profile"""
    try:
        artisan = Artisan.objects.get(user=request.user)
    except Artisan.DoesNotExist:
        return Response({'error': 'Artisan profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method in ['PUT', 'PATCH']:
        serializer = ArtisanUpdateSerializer(artisan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Return full artisan data after update
            return Response(ArtisanSerializer(artisan).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(ArtisanSerializer(artisan).data)
