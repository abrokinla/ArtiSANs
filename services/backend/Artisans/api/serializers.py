from rest_framework import serializers
from django.contrib.auth import get_user_model
from Artisans.models import Profile, Category, Artisan, JobRequest, Bid, Review, JobProgress, Transaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    role = serializers.ChoiceField(write_only=True, choices=['client', 'artisan'], required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 
                  'role', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Extract profile fields
        password = validated_data.pop('password')
        phone_number = validated_data.pop('phone_number', '')
        role = validated_data.pop('role', 'client')
        
        # Create user with role
        user = User.objects.create_user(**validated_data)
        user.role = role
        user.set_password(password)
        user.save()
        
        # Create or update profile with phone
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone_number = phone_number
        profile.save()
        
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArtisanSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.profile.phone_number', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Artisan
        fields = '__all__'
    
    def get_average_rating(self, obj):
        reviews = obj.reviews_received.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0


class ArtisanUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating artisan-specific fields"""
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Artisan
        fields = [
            'experience', 'whatsapp', 'tel', 'is_available',
            'available_days', 'available_hours_start', 'available_hours_end',
            'category_ids'
        ]
        extra_kwargs = {
            'experience': {'required': False},
            'whatsapp': {'required': False},
            'tel': {'required': False},
            'is_available': {'required': False},
            'available_days': {'required': False},
            'available_hours_start': {'required': False},
            'available_hours_end': {'required': False},
        }
    
    def update(self, instance, validated_data):
        # Handle categories separately
        category_ids = validated_data.pop('category_ids', None)
        if category_ids is not None:
            categories = Category.objects.filter(id__in=category_ids)
            instance.categories.set(categories)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class JobRequestSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username', read_only=True)
    artisan_username = serializers.CharField(source='artisan.user.username', read_only=True, allow_null=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    bids_count = serializers.SerializerMethodField()
    images = serializers.JSONField(required=False, default=list)

    class Meta:
        model = JobRequest
        fields = '__all__'
        read_only_fields = ('client', 'status', 'created_at', 'updated_at')

    def get_bids_count(self, obj):
        return obj.bids.count()


class BidSerializer(serializers.ModelSerializer):
    artisan_username = serializers.CharField(source='artisan.user.username', read_only=True)
    
    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ('artisan', 'created_at')


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    artisan_username = serializers.CharField(source='artisan.user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewer', 'artisan', 'job', 'created_at')


class JobProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProgress
        fields = '__all__'
        read_only_fields = ('artisan', 'created_at')


class TransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
