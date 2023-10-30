from django.urls import path
from django.views.generic.base import RedirectView
from .endpoints.artisan import ArtisanView, ArtisanRetrieveUpdateDestroyView
from .endpoints.profile import ProfileView, ProfileRetrieveUpdateDestroyView

urlpatterns = [
    # ---------------artisan url start------------------------
    path('artisans/', ArtisanView.as_view(), name='artisan-list'),
    path('artisans/<int:pk>/', ArtisanRetrieveUpdateDestroyView.as_view(), name='artisan-retrieve'),
    # ---------------artisan url end--------------------------

    # ---------------profile url start------------------------
    path('profile/', ProfileView.as_view(), name='client-list'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateDestroyView.as_view(), name='client-retrieve'),
    # ---------------profile url end--------------------------

    path('' , RedirectView.as_view(url='/'))
]