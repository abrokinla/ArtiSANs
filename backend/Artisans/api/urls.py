from django.urls import path
from django.views.generic.base import RedirectView
from .endpoints.artisan import ArtisanView, ArtisanRetrieveUpdateDestroyView
from .endpoints.profile import ProfileView, ProfileRetrieveUpdateDestroyView
from .endpoints.cat import CreateCategoryApiView, ListAllCategoryApiView, DetailUpdateDeleteCategoryApiView
from .endpoints.job import CreateJobRequestApiView, ListAllJobRequestApiView, DetailUpdateDeleteJobRequestApiView

urlpatterns = [
    # ---------------artisan url start------------------------
    path('artisans/', ArtisanView.as_view(), name='artisan-list'),
    path('artisans/<int:pk>/', ArtisanRetrieveUpdateDestroyView.as_view(), name='artisan-retrieve'),
    # ---------------artisan url end--------------------------

    # ---------------profile url start------------------------
    path('profile/', ProfileView.as_view(), name='client-list'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateDestroyView.as_view(), name='client-retrieve'),
    # ---------------profile url end--------------------------

    # ---------------category url start--------------------------
    path('caegory/create/', CreateCategoryApiView.as_view(), name='category-list'),
    path('category/list/', ListAllCategoryApiView.as_view(), name='list-all-category'),
    path('category/<int:pk>/', DetailUpdateDeleteCategoryApiView.as_view(), name='category-delete-retrieve'),
    # ---------------category url end-------------------------------

    # ---------------jobrequest url start--------------------------
    path('job/create/', CreateJobRequestApiView.as_view(), name='job-list'),
    path('job/list/', ListAllJobRequestApiView.as_view(), name='list-all-job'),
    path('job/<int:pk>/', DetailUpdateDeleteJobRequestApiView.as_view(), name='job-delete-retrieve'),
    # ---------------jobrequest url end-------------------------------

    path('' , RedirectView.as_view(url='/'))
]