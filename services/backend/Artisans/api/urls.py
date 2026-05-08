from django.urls import path
from django.views.generic.base import RedirectView
from .endpoints.artisan import CreateArtisanView, ListArtisanApiView, ArtisanRetrieveUpdateDestroyView, artisan_me_view
from .endpoints.profile import CreateProfileView, ListProfileApiView, ProfileRetrieveUpdateDestroyView
from .endpoints.cat import CreateCategoryApiView, ListAllCategoryApiView, DetailUpdateDeleteCategoryApiView
from .endpoints.job import CreateJobRequestApiView, ListUnassignedJobRequestApiView, DetailUpdateDeleteJobRequestApiView, ListAssignedJobRequestsView
from .endpoints.artisanscat import ListArtisansByCategoryView
from .endpoints.bid import BidViewSet
from .endpoints.review import ReviewViewSet
urlpatterns = [
    # ---------------artisan url start------------------------
    path('artisans/create/', CreateArtisanView.as_view(), name='artisan-create'),
    path('artisans/list/', ListArtisanApiView.as_view(), name='artisan-list'),
    path('artisans/<int:pk>/', ArtisanRetrieveUpdateDestroyView.as_view(), name='artisan-retrieve'),
    # ---------------artisan url end--------------------------
    
    # Artisan "me" endpoint for current user's profile
    path('artisans/me/', artisan_me_view, name='artisan-me'),
    
    # ---------------profile url start------------------------
    path('profile/create/', CreateProfileView.as_view(), name='client-create'),
    path('profile/list/', ListProfileApiView.as_view(), name='client-list'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateDestroyView.as_view(), name='client-retrieve'),
    # ---------------profile url end--------------------------

    # ---------------category url start--------------------------
    path('categories/create/', CreateCategoryApiView.as_view(), name='category-list'),
    path('categories/list/', ListAllCategoryApiView.as_view(), name='list-all-category'),
    path('categories/<int:pk>/', DetailUpdateDeleteCategoryApiView.as_view(), name='category-delete-retrieve'),
    # ---------------category url end-------------------------------

    # ---------------jobrequest url start--------------------------
    path('jobs/create/', CreateJobRequestApiView.as_view(), name='job-list'),
    path('jobs/list/', ListUnassignedJobRequestApiView.as_view(), name='list-all-job'),
    path('jobs/<int:pk>/', DetailUpdateDeleteJobRequestApiView.as_view(), name='job-delete-retrieve'),

    # URL for listing job requests assigned to a specific artisan
    path('jobs/assigned/<int:artisan_id>/', ListAssignedJobRequestsView.as_view(), name='list-assigned-job-requests'),

    # ---------------jobrequest url end-------------------------------

    # ---------------artisans in category url start--------------------------
    path('artisans/categories/<int:category_id>/', ListArtisansByCategoryView.as_view(), name='list-artisans-by-category'),
    # ---------------artisans in category url end--------------------------
    
    # ---------------bid url start--------------------------
    path('bids/', BidViewSet.as_view({'get': 'list', 'post': 'create'}), name='bid-list'),
    path('bids/<int:pk>/', BidViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='bid-detail'),
    path('bids/my/', BidViewSet.as_view({'get': 'my_bids'}), name='my-bids'),
    path('bids/job/', BidViewSet.as_view({'get': 'job_bids'}), name='job-bids'),
    path('bids/<int:pk>/accept/', BidViewSet.as_view({'post': 'accept'}), name='accept-bid'),
    # ---------------bid url end--------------------------
    
    # ---------------review url start--------------------------
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='review-detail'),
    path('reviews/artisan/', ReviewViewSet.as_view({'get': 'for_artisan'}), name='artisan-reviews'),
    # ---------------review url end--------------------------
    
    path('' , RedirectView.as_view(url='/'))
]