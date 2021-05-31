import json

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from rest_framework import viewsets, status, views, permissions
from rest_framework.generics import get_object_or_404

from api.filters import EventFilter
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
    filter_class = [EventFilter]


@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set."})


class UserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = get_object_or_404(MyUser, pk=request.user.id)
        return JsonResponse(data=MyUserSerializer(user).data)


@require_POST
def login_view(request, *args):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username is None or password is None:
        return JsonResponse({
            "error": "Please enter both username and password"
        }, status=400)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            "detail": "Success",
            "isStaff": user.is_staff,
            "username": user.username,
        })
    return JsonResponse(
        {"error": "Invalid credentials"},
        status=400,
    )


@login_required
def is_logged_in(request):
    user = request.user
    return JsonResponse({
        "detail": "success",
        "isStaff": user.is_staff,
        "username": user.username,
    })


@require_POST
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse(
        {"detail": "success"}
    )