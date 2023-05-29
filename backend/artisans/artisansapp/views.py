from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import User
from django.views.decorators.http import require_http_methods
from .forms import CreateUserForm

# Create your views here.
@require_http_methods(['POST'])
def create_user(request):
    if request.method == 'POST':
        data = request.POST

        form = CreateUserForm(data)

        if form.is_valid():
            # Create the new user instance
            new_user = form.save(commit=False)
            new_user.password = make_password(form.cleaned_data['password'])
            new_user.save()

            return JsonResponse({
                'success': True,
                'message': 'User created successfully',
                'user': new_user.id
            }, status=201)
        else:
            return JsonResponse({
                'error': form.errors
            }, status=400)

    # If the request method is not POST, return an error response
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)