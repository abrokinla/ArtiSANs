from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.serializers import UserSerializer, ProfileSerializer
from Artisans.models import Profile

class CreateProfileView(generics.CreateAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            profile_data = request.data.copy()
            user_data = profile_data.pop('user')

            user_serializer = UserSerializer(data=user_data)
            profile_serializer = ProfileSerializer(data=profile_data)

            user_serializer.is_valid(raise_exception=True)
            profile_serializer.is_valid(raise_exception=True)

            user = user_serializer.save()
            profile_data['user'] = user.id
            profile_serializer.save(user=user)

            return Response({
                'success':True,
                'data': profile_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:

            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ListProfileApiView(generics.ListAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return response({
                'success': False,
                'message': 'No records found'
            }, status=status.HTTP_404_NOT_FOUND)

        profile_serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': profile_serializer.data
        }, status=status.HTTP_200_OK)


class ProfileRetrieveUpdateDestroyView(
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            return Response({
                'success': False,
                'message': 'No record found'
            }, status=status.HTTP_404_NOT_FOUND)

        profile_serializer = self.get_serializer(instance, data=request.data, partial=True)

        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()

            user_data = request.data.get('user')
            if user_data:
                user = instance.user
                user_serializer = UserSerializer(instance=user_data, partial=True)

                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()

            return Response({
                'success': True,
                'data': profile_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': profile_serializer.errors
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

        profile_serializer = self.get_serializer(instance)
        user_serializer = UserSerializer(instance=instance.user)

        return Response({
            'success': True,
            'data':{
                'artisan': profile_serializer.data,
                'user': user_serializer.data
            }
        }, status=status.HTTP_200_OK)


