from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.endpoints.artisan import AuthViewSet, ArtisanViewSet, CategoryViewSet
from api.endpoints.job import JobViewSet
from api.endpoints.profile import ProfileViewSet
from api.endpoints.review import ReviewViewSet
from api.endpoints.progress import JobProgressViewSet
from api.endpoints.search import SearchViewSet
from api.endpoints.bid import BidViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'artisans', ArtisanViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'progress', JobProgressViewSet)
router.register(r'bids', BidViewSet)

# Search doesn't need a router since it's a ViewSet with only @action methods
search_viewset = SearchViewSet.as_view({
    'get': 'artisans'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/search/', include([
        path('artisans/', search_viewset),
        path('categories/', SearchViewSet.as_view({'get': 'categories'})),
        path('nearby/', SearchViewSet.as_view({'get': 'nearby'})),
        path('trending/', SearchViewSet.as_view({'get': 'trending'})),
    ])),
    path('api-auth/', include('rest_framework.urls')),
]
