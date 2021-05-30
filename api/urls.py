from django.urls import path
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()
router.register(r"gender", GenderViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"registered-staffs", RegisteredStaffViewSet)
router.register(r"clothes-settings", ClothesSettingViewSet)
router.register(r"gathering-place-settings", GatheringPlaceSettingViewSet)
router.register(r"position-data", PositionDataViewSet)
router.register(r"positions", PositionViewSet)
router.register(r"position-groups", PositionGroupViewSet)
router.register(r"events", EventViewSet)

urlpatterns = router.urls + [
    path("set-csrf-token/", set_csrf_token)
]
