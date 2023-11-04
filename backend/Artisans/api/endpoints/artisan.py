from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.serializers import UserSerializer, ArtisansSerializer
from Artisans.models import Artisan

class CreateArtisanView(generics.CreateAPIView):

    queryset = Artisan.objects.all()
    serializer_class = ArtisansSerializer

    def create(self, request, *args, **kwargs):
        try:
            artisan_data = request.data.copy()
            user_data = artisan_data.pop('user')

            user_serializer = UserSerializer(data=user_data)
            artisan_serializer = ArtisansSerializer(data=artisan_data)

            user_serializer.is_valid(raise_exception=True)
            artisan_serializer.is_valid(raise_exception=True)

            user = user_serializer.save()
            artisan_data['user'] = user.id
            artisan_serializer.save(user=user)

            return Response({
                'success':True,
                'data': artisan_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:

            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ListArtisanApiView(generics.ListAPIView):
    queryset = Artisan.objects.all()
    serializer_class = ArtisansSerializer

    def list(self, request, *args, **kwargs):
        if request.method == 'POST':
            return None
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return response({
                'success': False,
                'message': 'No records found'
            }, status=status.HTTP_404_NOT_FOUND)

        artisan_serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': artisan_serializer.data
        }, status=status.HTTP_200_OK)


class ArtisanRetrieveUpdateDestroyView(
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView):

    queryset = Artisan.objects.all()
    serializer_class = ArtisansSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            return Response({
                'success': False,
                'message': 'No record found'
            }, status=status.HTTP_404_NOT_FOUND)

        artisan_serializer = self.get_serializer(instance, data=request.data, partial=True)

        if artisan_serializer.is_valid(raise_exception=True):
            artisan_serializer.save()

            user_data = request.data.get('user')
            if user_data:
                user = instance.user
                user_serializer = UserSerializer(instance=user_data, partial=True)

                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()

            return Response({
                'success': True,
                'data': artisan_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': artisan_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            return Response({
                'success': False,
                'message': 'Record not Found'
            }, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)

        return Response({
            'success': True,
            'message': 'Record Deleted!'
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:

            return Response({
                'success': False,
                'message': 'Record not Found!'
            }, status=status.HTTP_404_NOT_FOUND)

        artisan_serializer = self.get_serializer(instance)
        user_serializer = UserSerializer(instance=instance.user)

        return Response({
            'success': True,
            'data':{
                'artisan': artisan_serializer.data,
                'user': user_serializer.data
            }
        }, status=status.HTTP_200_OK)


