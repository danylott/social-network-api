from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet, PostViewSet, LikeViewSet, ProfileViewSet, JWTAuthenticationView

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('likes', LikeViewSet)
router.register('profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', JWTAuthenticationView.as_view(), name='jwt_token'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]