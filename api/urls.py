from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path("set-csrf-token/", set_csrf_token),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("get-user/", UserView.as_view(), name="get_user"),
    path("login/", login_view, name="login"),
    path("check-user/", is_logged_in, name="check_user"),
    path("logout/", logout_view, name="logout"),
    path("available-staffs/", AvailableStaffsView.as_view(), name="available staffs")
]
