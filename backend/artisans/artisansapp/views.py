from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import User
from django.views.decorators.http import require_http_methods
from .forms import UserForm, ArtisanForm

# Create your views here.
@require_http_methods(['POST'])
def create_user(request):
    if request.method == 'POST':
        data = request.POST

        user_form = UserForm(data)
        artisan_form = ArtisanForm(data)

        if user_form.is_valid():
            # Create the new user instance
            new_user = user_form.save(commit=False)
            new_user.password = make_password(user_form.cleaned_data['password'])
            new_user.save()

            # Check if the user is an artisan and save artisan-specific details
            if new_user.role == 'artisan' and artisan_form.is_valid():
                artisan = artisan_form.save(commit=False)
                artisan.user = new_user
                artisan.save()

            return JsonResponse({
                'success': True,
                'message': 'User created successfully',
                'user': new_user.id
            }, status=200)
        else:
            return JsonResponse({
                'user_errors': user_form.errors,
                'artisan_errors': artisan_form.errors
            }, status=400)

    # If the request method is not POST, return an error response
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)