from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('artisan', 'Artisan'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    
    # NIN/BVN verification fields (Nigeria-first)
    nin_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    bvn_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    nin_verified = models.BooleanField(default=False)
    bvn_verified = models.BooleanField(default=False)
    verification_doc = models.FileField(upload_to='verifications/', null=True, blank=True)
    
    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(Group, related_name='artisans_user_set')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='artisans_user_set',
        verbose_name='user permissions',
        blank=True,
    )

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    profile_picture_url = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    # Subscription tier
    SUBSCRIPTION_CHOICES = (
        ('basic', 'Basic (Free)'),
        ('pro', 'Pro (₦5,000/mo)'),
        ('premium', 'Premium (₦15,000/mo)'),
    )
    subscription_tier = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='basic')
    subscription_expires = models.DateField(null=True, blank=True)
    bids_remaining = models.IntegerField(default=3)  # Basic: 3/month, Pro: 15/month, Premium: unlimited

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, default='')
    icon = models.CharField(max_length=50, default='')  # FontAwesome icon class

    def __str__(self):
        return self.name


class Artisan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'artisan'})
    categories = models.ManyToManyField(Category)
    
    bio = models.TextField(default='')
    experience = models.TextField(default='')
    location = models.CharField(max_length=200, default='')
    whatsapp = models.CharField(max_length=20, default='', blank=True)
    tel = models.CharField(max_length=20, default='', blank=True)
    
    # Verification & trust
    is_verified = models.BooleanField(default=False)
    verification_badge = models.BooleanField(default=False)
    
    # Availability
    is_available = models.BooleanField(default=True)
    available_days = models.CharField(max_length=50, default='Mon,Tue,Wed,Thu,Fri')  # Comma-separated
    available_hours_start = models.TimeField(default='08:00')
    available_hours_end = models.TimeField(default='18:00')
    
    # Portfolio
    portfolio_images = models.JSONField(default=list, blank=True)  # List of image URLs
    
    # Earnings
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pending_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username


class JobRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('bidding', 'Open for Bids'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    )
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_requests', limit_choices_to={'role': 'client'})
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_jobs')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Location
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Budget
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Escrow & Payment
    escrow_id = models.CharField(max_length=100, null=True, blank=True)  # Paystack escrow ID
    escrow_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_escrow_released = models.BooleanField(default=False)
    
    # Commission
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # 10% default
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Lead fee (if applicable)
    lead_fee_paid = models.BooleanField(default=False)
    lead_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Calculate commission when final_amount is set
        if self.final_amount and self.commission_rate:
            self.commission_amount = (self.final_amount * self.commission_rate) / 100
        super().save(*args, **kwargs)


class Bid(models.Model):
    job = models.ForeignKey(JobRequest, on_delete=models.CASCADE, related_name='bids')
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(null=True, blank=True)
    estimated_days = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('job', 'artisan')  # One bid per artisan per job
    
    def __str__(self):
        return f"{self.artisan.user.username} bid on {self.job.title}"


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # 1-5 stars
    
    job = models.OneToOneField(JobRequest, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given', limit_choices_to={'role': 'client'})
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, related_name='reviews_received')
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # For dispute resolution
    is_disputed = models.BooleanField(default=False)
    dispute_reason = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.reviewer.username} rated {self.artisan.user.username} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update artisan's average rating
        from django.db.models import Avg
        avg_rating = Review.objects.filter(artisan=self.artisan).aggregate(Avg('rating'))['rating__avg']
        # You might want to store this on the Artisan model for performance


class JobProgress(models.Model):
    job = models.ForeignKey(JobRequest, on_delete=models.CASCADE, related_name='progress_updates')
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    description = models.TextField()
    images = models.JSONField(default=list, blank=True)  # List of image URLs
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Progress update for {self.job.title}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('escrow_hold', 'Escrow Hold'),
        ('escrow_release', 'Escrow Release'),
        ('commission', 'Commission Deduction'),
        ('lead_fee', 'Lead Fee'),
        ('subscription', 'Subscription Payment'),
        ('verification_fee', 'Verification Fee'),
        ('payout', 'Artisan Payout'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Successful'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)  # Paystack reference
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    job = models.ForeignKey(JobRequest, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₦{self.amount}"
