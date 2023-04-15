from django.db.models import query
from django.http import request
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.models import *
from .serializers import *

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class GetUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class GetUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class SetLocationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data['tg_id']
        floor = request.data['floor']
        x = request.data['x']
        y = request.data['y']

        user = User.objects.get(tg_id=user_id)
        user.last_time_set_location = datetime.datetime.now()
        user.location = Location.objects.get_or_create(floor=Floor.objects.get(number=floor), x=x, y=y)[0]
        user.save()

        return Response(status=status.HTTP_200_OK)


class GetFloorsView(generics.ListAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [AllowAny]


class GetInterestsView(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [AllowAny]


class CreateInterestView(generics.CreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [AllowAny]


class SetView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from_id = request.data['from_id']
        target_id = request.data['target_id']
        
        from_user = User.objects.get(tg_id=from_id)
        target_user = User.objects.get(tg_id=target_id)
        
        view = ProfileView.objects.create(from_user=from_user, target_user=target_user)
        view.save()

        return Response(status=status.HTTP_200_OK)


class MapView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        floor = request.GET.get('floor')
        user = User.objects.get(tg_id=request.GET.get('tg_id'))
        floor = Floor.objects.get(number=floor)
        data = {
            'map_image': floor.map_image.url,
            'map_height': floor.map_image.height,
            'map_width': floor.map_image.width,
            'zoom_x': 1,
            'zoom_y': 1,
            'users': MapSerializer(User.objects.filter(location__floor=floor, 
                    last_time_set_location__gt=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(tg_id=user.tg_id),
                    many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)


class InCoworkingView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(tg_id=request.GET.get('tg_id'))
        data = UserSerializer(User.objects.filter(last_time_set_location__gt=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(tg_id=user.tg_id), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class GetAllUsersView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(tg_id=request.GET.get('tg_id'))
        data = UserSerializer(User.objects.exclude(tg_id=user.tg_id), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class SkipUserView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = User.objects.get(tg_id=request.data['tg_id'])
        user.blacklist.add(User.objects.get(tg_id=request.data['target_id']))
        return Response(status=status.HTTP_200_OK)
