from django.urls import path
from django.views.generic.base import RedirectView
# from .endpoints.

urlpatterns = [

    path('' , RedirectView.as_view(url='/'))
]
