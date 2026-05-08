from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from Artisans.models import Bid, JobRequest, Artisan
from api.serializers import BidSerializer
from django.shortcuts import get_object_or_404

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'artisan':
            # Artisans see their own bids
            try:
                artisan = Artisan.objects.get(user=user)
                return Bid.objects.filter(artisan=artisan)
            except Artisan.DoesNotExist:
                return Bid.objects.none()
        else:
            # Clients see bids on their jobs
            return Bid.objects.filter(job__client=user)
    
    def perform_create(self, serializer):
        """Artisan places a bid on a job"""
        user = self.request.user
        if user.role != 'artisan':
            raise PermissionDenied("Only artisans can place bids")
        
        try:
            artisan = Artisan.objects.get(user=user)
        except Artisan.DoesNotExist:
            raise PermissionDenied("Artisan profile not found")
        
        # Check if job exists and is open for bidding
        job_id = self.request.data.get('job')
        job = get_object_or_404(JobRequest, id=job_id)
        
        if job.status not in ['pending', 'bidding']:
            raise PermissionDenied("Job is not open for bidding")
        
        # Check if artisan already bid on this job
        if Bid.objects.filter(job=job, artisan=artisan).exists():
            raise PermissionDenied("You have already bid on this job")
        
        # Check subscription limits
        if user.profile.subscription_tier == 'basic':
            if user.profile.bids_remaining <= 0:
                raise PermissionDenied("No bids remaining. Upgrade to Pro for more bids.")
        
        serializer.save(artisan=artisan, job=job)
        
        # Deduct bid count for basic tier
        if user.profile.subscription_tier == 'basic':
            user.profile.bids_remaining -= 1
            user.profile.save()
        
        # Update job status to bidding if still pending
        if job.status == 'pending':
            job.status = 'bidding'
            job.save()
    
    @action(detail=False, methods=['get'])
    def my_bids(self, request):
        """List current artisan's bids"""
        try:
            artisan = Artisan.objects.get(user=request.user)
            bids = Bid.objects.filter(artisan=artisan)
            return Response(self.get_serializer(bids, many=True).data)
        except Artisan.DoesNotExist:
            return Response({'error': 'Artisan profile not found'}, status=404)
    
    @action(detail=False, methods=['get'])
    def job_bids(self, request):
        """List all bids for a specific job (client only)"""
        job_id = request.query_params.get('job_id')
        if not job_id:
            return Response({'error': 'job_id required'}, status=400)
        
        try:
            job = JobRequest.objects.get(id=job_id, client=request.user)
        except JobRequest.DoesNotExist:
            return Response({'error': 'Job not found or unauthorized'}, status=404)
        
        bids = Bid.objects.filter(job=job)
        return Response(self.get_serializer(bids, many=True).data)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Client accepts a bid and assigns the job"""
        bid = self.get_object()
        
        # Verify the client owns this job
        if bid.job.client != request.user:
            return Response({'error': 'Unauthorized'}, status=403)
        
        # Check job is still open
        if bid.job.status not in ['pending', 'bidding']:
            return Response({'error': 'Job is no longer open'}, status=400)
        
        # Accept this bid
        bid.is_accepted = True
        bid.save()
        
        # Update job
        job = bid.job
        job.artisan = bid.artisan
        job.status = 'assigned'
        job.final_amount = bid.amount
        job.save()
        
        # Reject other bids
        Bid.objects.filter(job=job).exclude(id=bid.id).update(is_accepted=False)
        
        return Response({'message': 'Bid accepted, job assigned'})
