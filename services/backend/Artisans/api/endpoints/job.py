from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from Artisans.models import JobRequest, Bid, Artisan, Transaction
from api.serializers import JobRequestSerializer, BidSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid
import cloudinary.uploader

class JobViewSet(viewsets.ModelViewSet):
    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        
        # For unauthenticated users, show only open/bidding jobs
        if not user.is_authenticated:
            return JobRequest.objects.filter(status__in=['open', 'bidding'])
        
        # For authenticated users, filter by their role
        if user.role == 'client':
            return JobRequest.objects.filter(client=user)
        elif user.role == 'artisan':
            try:
                artisan = Artisan.objects.get(user=user)
                return JobRequest.objects.filter(artisan=artisan) | JobRequest.objects.filter(status='bidding')
            except Artisan.DoesNotExist:
                return JobRequest.objects.none()
        return JobRequest.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=False, methods=['post'], url_path='upload_image')
    def upload_job_image(self, request):
        """Upload a job image to Cloudinary and return the URL"""
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
        if image_file.content_type not in allowed_types:
            return Response(
                {'error': f'Invalid file type: {image_file.content_type}. Allowed: JPEG, PNG, WebP, GIF'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate file size (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            return Response(
                {'error': 'File too large. Maximum size is 5MB'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder='artisans/job_images',
                overwrite=True,
                resource_type='image',
                transformation=[
                    {'width': 1200, 'height': 1200, 'crop': 'limit'},
                    {'quality': 'auto:good'},
                    {'fetch_format': 'auto'}
                ]
            )

            return Response({
                'url': upload_result['secure_url'],
                'public_id': upload_result['public_id'],
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def open_bidding(self, request, pk=None):
        """Open job for bidding"""
        job = self.get_object()
        if job.client != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        job.status = 'bidding'
        job.save()
        return Response({'message': 'Job opened for bidding'})
    
    @action(detail=True, methods=['post'])
    def bid(self, request, pk=None):
        """Submit a bid for a job (artisan only)"""
        if request.user.role != 'artisan':
            return Response({'error': 'Only artisans can bid'}, status=status.HTTP_403_FORBIDDEN)
        
        job = self.get_object()
        if job.status != 'bidding':
            return Response({'error': 'Job is not open for bidding'}, status=status.HTTP_400_BAD_REQUEST)
        
        artisan = get_object_or_404(Artisan, user=request.user)
        
        # Check subscription limits
        if artisan.user.profile.subscription_tier == 'basic' and artisan.user.profile.bids_remaining <= 0:
            return Response({'error': 'No bids remaining. Upgrade your subscription.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if already bid
        if Bid.objects.filter(job=job, artisan=artisan).exists():
            return Response({'error': 'You have already bid on this job'}, status=status.HTTP_400_BAD_REQUEST)
        
        bid = Bid.objects.create(
            job=job,
            artisan=artisan,
            amount=request.data.get('amount'),
            message=request.data.get('message', ''),
            estimated_days=request.data.get('estimated_days', 1)
        )
        
        # Decrement bids remaining for basic tier
        if artisan.user.profile.subscription_tier == 'basic':
            artisan.user.profile.bids_remaining -= 1
            artisan.user.profile.save()
        
        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def accept_bid(self, request, pk=None):
        """Accept a bid and assign artisan (client only)"""
        job = self.get_object()
        if job.client != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        bid_id = request.data.get('bid_id')
        bid = get_object_or_404(Bid, id=bid_id, job=job)
        
        # Assign artisan and update job
        job.artisan = bid.artisan
        job.status = 'assigned'
        job.final_amount = bid.amount
        job.save()
        
        # Mark bid as accepted
        bid.is_accepted = True
        bid.save()
        
        # Create escrow (mock for MVP - integrate Paystack later)
        job.escrow_amount = bid.amount
        job.escrow_id = f"mock_escrow_{uuid.uuid4().hex[:8]}"
        job.save()
        
        return Response({'message': 'Bid accepted. Escrow created.', 'job': JobRequestSerializer(job).data})
    
    @action(detail=True, methods=['post'])
    def start_job(self, request, pk=None):
        """Start the job (artisan only)"""
        job = self.get_object()
        if not job.artisan or job.artisan.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        job.status = 'in_progress'
        job.save()
        return Response({'message': 'Job started'})
    
    @action(detail=True, methods=['post'])
    def complete_job(self, request, pk=None):
        """Mark job as complete (artisan only)"""
        job = self.get_object()
        if not job.artisan or job.artisan.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        job.status = 'completed'
        job.completed_at = timezone.now()
        job.save()
        return Response({'message': 'Job marked as complete. Awaiting client confirmation.'})
    
    @action(detail=True, methods=['post'])
    def confirm_completion(self, request, pk=None):
        """Confirm job completion and release escrow (client only)"""
        job = self.get_object()
        if job.client != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if job.status != 'completed':
            return Response({'error': 'Job must be marked complete first'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate commission
        commission = (job.final_amount * job.commission_rate) / 100
        
        # Release escrow (mock - integrate Paystack API later)
        job.is_escrow_released = True
        job.commission_amount = commission
        job.save()
        
        # Update artisan earnings
        artisan = job.artisan
        artisan.total_earnings += (job.final_amount - commission)
        artisan.save()
        
        # Record transaction
        Transaction.objects.create(
            user=artisan.user,
            transaction_type='escrow_release',
            amount=job.final_amount - commission,
            reference=f"release_{uuid.uuid4().hex[:8]}",
            status='success',
            job=job
        )
        
        return Response({'message': 'Job completed. Payment released to artisan.', 'commission': str(commission)})
    
    @action(detail=True, methods=['post'])
    def dispute(self, request, pk=None):
        """Raise a dispute (client or artisan)"""
        job = self.get_object()
        if job.client != request.user and (not job.artisan or job.artisan.user != request.user):
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        job.status = 'disputed'
        job.save()
        # Here you'd notify admin or create a dispute record
        return Response({'message': 'Dispute raised. Admin will review.'})
    
    @action(detail=False, methods=['get'])
    def my_jobs(self, request):
        """Get jobs for current user"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
