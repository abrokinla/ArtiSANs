from django import forms
from  ..models import User, Artisan

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'role']

class ArtisanForm(forms.ModelForm):
    class Meta:
        model = Artisan
        fields = ['bio', 'experience', 'location', 'whatsapp', 'tel']

