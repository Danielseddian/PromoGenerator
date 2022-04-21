from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import PromoViewSet, CheckView, CreateUserView

router = DefaultRouter()
router.register("promo", PromoViewSet, basename="promos")
router.register("check", CheckView, basename="check")
router.register("signup", CreateUserView, basename="signup")


urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
