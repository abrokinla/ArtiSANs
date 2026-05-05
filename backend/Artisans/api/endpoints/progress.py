from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Artisans.models import JobProgress, JobRequest, Artisan
from api.serializers import JobProgressSerializer
from django.shortcuts import get_object_or_404

class JobProgressViewSet(viewsets.ModelViewSet):
    queryset = JobProgress.objects.all()
    serializer_class = JobProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'artisan':
            try:
                artisan = Artisan.objects.get(user=user)
                return JobProgress.objects.filter(artisan=artisan)
            except Artisan.DoesNotExist:
                return JobProgress.objects.none()
        elif user.role == 'client':
            # Clients can see progress on their jobs
            client_jobs = JobRequest.objects.filter(client=user)
            return JobProgress.objects.filter(job__in=client_jobs)
        return JobProgress.objects.none()
    
    def perform_create(self, serializer):
        """Add progress update to a job (artisan only)"""
        job_id = self.request.data.get('job')
        job = get_object_or_404(JobRequest, id=job_id)
        
        if not job.artisan or job.artisan.user != self.request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if job.status != 'in_progress':
            return Response({'error': 'Job must be in progress'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(artisan=job.artisan, job=job)
    
    @action(detail=False, methods=['get'])
    def by_job(self, request):
        """Get all progress updates for a specific job"""
        job_id = request.query_params.get('job_id')
        if not job_id:
            return Response({'error': 'job_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        job = get_object_or_404(JobRequest, id=job_id)
        
        # Check authorization
        if job.client != request.user and (not job.artisan or job.artisan.user != request.user):
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        progress = JobProgress.objects.filter(job=job).order_by('-created_at')
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)
