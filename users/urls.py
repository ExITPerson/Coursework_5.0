from rest_framework.routers import DefaultRouter
from django.urls import path

from users.apps import UsersConfig
from users.views import UserViewSet, CustomTokenObtainPairView

from rest_framework_simplejwt.views import TokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
