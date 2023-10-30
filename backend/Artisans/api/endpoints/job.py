from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.serializers import JobRequestSerializer
from Artisans.models import JobRequest


# create category:
class CreateJobRequestApiView(generics.CreateAPIView):
    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer


# list all courses:
class ListAllJobRequestApiView(generics.ListAPIView):
    queryset = JobRequest.objects.all()
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