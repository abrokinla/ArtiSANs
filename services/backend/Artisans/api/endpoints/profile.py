from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Artisans.models import Profile, User, Transaction
from api.serializers import ProfileSerializer, UserSerializer, TransactionSerializer
from django.shortcuts import get_object_or_404
import uuid

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile"""
        profile = get_object_or_404(Profile, user=request.user)
        
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def upgrade_subscription(self, request):
        """Upgrade subscription tier (MVP - mock payment)"""
        tier = request.data.get('tier')
        if tier not in ['basic', 'pro', 'premium']:
            return Response({'error': 'Invalid tier'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile = request.user.profile
        profile.subscription_tier = tier
        
        # Mock payment - in production, integrate Paystack/Flutterwave
        if tier == 'pro':
            profile.subscription_expires = timezone.now() + timezone.timedelta(days=30)
            profile.bids_remaining = 15
        elif tier == 'premium':
            profile.subscription_expires = timezone.now() + timezone.timedelta(days=30)
            profile.bids_remaining = 999  # Unlimited
        
        profile.save()
        
        # Record transaction (mock)
        Transaction.objects.create(
            user=request.user,
            transaction_type='subscription',
            amount=5000.00 if tier == 'pro' else 15000.00,
            reference=f"sub_{uuid.uuid4().hex[:8]}",
            status='success'
        )
        
        return Response({
            'message': f'Upgraded to {tier} tier',
            'profile': ProfileSerializer(profile).data
        })
    
    @action(detail=False, methods=['get'])
    def transactions(self, request):
        """Get current user's transaction history"""
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def verify_identity(self, request):
        """Submit ID verification documents (mock for MVP)"""
        profile = request.user.profile
        verification_type = request.data.get('type')  # 'nin' or 'bvn'
        
        if verification_type == 'nin':
            request.user.nin_verified = True
            request.user.save()
        elif verification_type == 'bvn':
            request.user.bvn_verified = True
            request.user.save()
        else:
            return Response({'error': 'Invalid verification type'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': f'{verification_type.upper()} verification submitted'})
    
    @action(detail=False, methods=['get'])
    def usage_stats(self, request):
        """Get usage statistics for current user"""
        user = request.user
        stats = {}
        
        if user.role == 'artisan':
            from Artisans.models import Artisan, JobRequest, Bid
            try:
                artisan = Artisan.objects.get(user=user)
                stats = {
                    'total_jobs': JobRequest.objects.filter(artisan=artisan).count(),
                    'completed_jobs': JobRequest.objects.filter(artisan=artisan, status='completed').count(),
                    'total_bids': Bid.objects.filter(artisan=artisan).count(),
                    'bids_remaining': user.profile.bids_remaining,
                    'subscription_tier': user.profile.subscription_tier,
                    'total_earnings': str(artisan.total_earnings),
                    'pending_earnings': str(artisan.pending_earnings),
                }
            except Artisan.DoesNotExist:
                stats = {'error': 'Artisan profile not found'}
        
        elif user.role == 'client':
            from Artisans.models import JobRequest
            stats = {
                'total_jobs_posted': JobRequest.objects.filter(client=user).count(),
                'active_jobs': JobRequest.objects.filter(client=user, status__in=['assigned', 'in_progress']).count(),
                'completed_jobs': JobRequest.objects.filter(client=user, status='completed').count(),
            }
        
        return Response(stats)
