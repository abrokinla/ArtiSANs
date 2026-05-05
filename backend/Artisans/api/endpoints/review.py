from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from Artisans.models import Review, JobRequest, Artisan
from api.serializers import ReviewSerializer
from django.shortcuts import get_object_or_404

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)
    
    def perform_create(self, serializer):
        """Client creates a review for a completed job"""
        user = self.request.user
        if user.role != 'client':
            raise PermissionDenied("Only clients can write reviews")
        
        job_id = self.request.data.get('job')
        job = get_object_or_404(JobRequest, id=job_id, client=user)
        
        # Job must be completed
        if job.status != 'completed':
            raise PermissionDenied("Can only review completed jobs")
        
        # Check if review already exists
        if Review.objects.filter(job=job).exists():
            raise PermissionDenied("Review already exists for this job")
        
        serializer.save(reviewer=user, artisan=job.artisan, job=job)
    
    @action(detail=False, methods=['get'])
    def for_artisan(self, request):
        """Get all reviews for a specific artisan"""
        artisan_id = request.query_params.get('artisan_id')
        if not artisan_id:
            return Response({'error': 'artisan_id required'}, status=400)
        
        try:
            artisan = Artisan.objects.get(id=artisan_id)
        except Artisan.DoesNotExist:
            return Response({'error': 'Artisan not found'}, status=404)
        
        reviews = Review.objects.filter(artisan=artisan)
        return Response(self.get_serializer(reviews, many=True).data)
