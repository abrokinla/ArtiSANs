from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.serializers import CategorySerializer
from Artisans.models import Category


# create category:
class CreateCategoryApiView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# list all courses:
class ListAllCategoryApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# get, update or delete a single category
class DetailUpdateDeleteCategoryApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field is the field that is used to retrieve the object
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': 'Category deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)