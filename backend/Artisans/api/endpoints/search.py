from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from Artisans.models import Artisan, Category, JobRequest
from api.serializers import ArtisanSerializer, CategorySerializer
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404

class SearchViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def artisans(self, request):
        """Search artisans by location, category, rating"""
        queryset = Artisan.objects.filter(is_available=True)
        
        # Filters
        category = request.query_params.get('category')
        location = request.query_params.get('location')
        min_rating = request.query_params.get('min_rating')
        max_budget = request.query_params.get('max_budget')
        availability = request.query_params.get('availability')  # 'today', 'this_week', 'weekends'
        
        if category:
            queryset = queryset.filter(categories__name__icontains=category)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_rating:
            # This is a simplified approach - in production, use annotate/aggregate
            queryset = queryset.filter(reviews_received__rating__gte=float(min_rating))
        if availability:
            from datetime import datetime
            now = datetime.now()
            if availability == 'today':
                # Check if artisan is available today
                today = now.strftime('%a')[:3]  # 'Mon', 'Tue', etc.
                queryset = queryset.filter(available_days__icontains=today)
        
        # Order by rating
        queryset = queryset.distinct()
        
        # Calculate average rating for each artisan
        results = []
        for artisan in queryset:
            reviews = artisan.reviews_received.all()
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            review_count = reviews.count()
            
            results.append({
                'id': artisan.id,
                'username': artisan.user.username,
                'first_name': artisan.user.first_name,
                'last_name': artisan.user.last_name,
                'location': artisan.location,
                'categories': [cat.name for cat in artisan.categories.all()],
                'average_rating': round(avg_rating, 1),
                'review_count': review_count,
                'is_verified': artisan.is_verified,
                'verification_badge': artisan.verification_badge,
                'bio': artisan.bio[:100] + '...' if len(artisan.bio) > 100 else artisan.bio,
            })
        
        # Sort by rating
        results.sort(key=lambda x: x['average_rating'], reverse=True)
        
        return Response(results)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """List all categories with artisan counts"""
        categories = Category.objects.all()
        result = []
        for cat in categories:
            result.append({
                'id': cat.id,
                'name': cat.name,
                'description': cat.description,
                'artisan_count': cat.artisan_set.filter(is_available=True).count()
            })
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Search artisans near a location (simplified - text-based for MVP)"""
        latitude = request.query_params.get('lat')
        longitude = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 10))  # km
        category = request.query_params.get('category')
        
        if not latitude or not longitude:
            return Response({'error': 'lat and lng required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # For MVP, use text-based location matching
        # In production, use PostGIS or similar for geospatial queries
        queryset = Artisan.objects.filter(is_available=True)
        
        if category:
            queryset = queryset.filter(categories__name__icontains=category)
        
        # Return all matching artisans (location-based filtering would need lat/lng on model)
        serializer = ArtisanSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending artisans (most bids/reviews in last 30 days)"""
        from django.utils import timezone
        from datetime import timedelta
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Get artisans with most bids in last 30 days
        trending = Artisan.objects.filter(
            is_available=True,
            bids__created_at__gte=thirty_days_ago
        ).distinct()
        
        serializer = ArtisanSerializer(trending[:10], many=True)
        return Response(serializer.data)
