from django.contrib import admin
from .models import User, Artisan, JobRequest, Category, Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Artisan)
admin.site.register(JobRequest)
admin.site.register(Category)
admin.site.register(Profile)

