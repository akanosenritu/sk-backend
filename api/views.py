import jwt
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, status, views, permissions
from rest_framework.generics import get_object_or_404

from api.models import *
from api.serializers import RegisteredStaffSerializer, ClothesSettingSerializer, GatheringPlaceSettingSerializer, \
    PositionDataSerializer, PositionSerializer, PositionGroupSerializer, EventSerializer, EmployeeSerializer, \
    GenderSerializer, MyUserSerializer
from skbackend import settings


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    

class RegisteredStaffViewSet(viewsets.ModelViewSet):
    queryset = RegisteredStaff.objects.all()
    serializer_class = RegisteredStaffSerializer
    
    
class ClothesSettingViewSet(viewsets.ModelViewSet):
    queryset = ClothesSetting.objects.all()
    serializer_class = ClothesSettingSerializer
    
    
class GatheringPlaceSettingViewSet(viewsets.ModelViewSet):
    queryset = GatheringPlaceSetting.objects.all()
    serializer_class = GatheringPlaceSettingSerializer


class PositionDataViewSet(viewsets.ModelViewSet):
    queryset = PositionData.objects.all()
    serializer_class = PositionDataSerializer
    
    
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionGroupViewSet(viewsets.ModelViewSet):
    queryset = PositionGroup.objects.all()
    serializer_class = PositionGroupSerializer
    

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set."})


class UserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = get_object_or_404(MyUser, pk=request.user.id)
        return JsonResponse(data=MyUserSerializer(user).data)
