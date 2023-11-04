from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.serializers import JobRequestSerializer
from Artisans.models import JobRequest


# create job request:
class CreateJobRequestApiView(generics.CreateAPIView):
    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer


# list all job requests that are not assigned to any artisan:
class ListUnassignedJobRequestApiView(generics.ListAPIView):
    queryset = JobRequest.objects.filter(artisan__isnull=True)
    serializer_class = JobRequestSerializer


# get, update or delete a single category
class DetailUpdateDeleteJobRequestApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer
    # lookup_field is the field that is used to retrieve the object
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': 'Job request deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)

class ListAssignedJobRequestsView(generics.ListAPIView):
    serializer_class = JobRequestSerializer

    def get_queryset(self):
        # Retrieve the artisan_id from the URL parameter
        artisan_id = self.kwargs.get('artisan_id')

        # Filter job requests assigned to the specified artisan
        return JobRequest.objects.filter(artisan_id=artisan_id)