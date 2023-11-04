from rest_framework import generics, status
from rest_framework.response import Response
from api.serializers import ArtisansSerializer
from Artisans.models import Artisan, Category

# List Artisans by Category View
class ListArtisansByCategoryView(generics.ListAPIView):
    serializer_class = ArtisansSerializer

    def get_queryset(self):
        # Retrieve the category_id from the URL parameter
        category_id = self.kwargs.get('category_id')

        # Use the category_id to filter artisans by category
        return Artisan.objects.filter(categories__id=category_id)
