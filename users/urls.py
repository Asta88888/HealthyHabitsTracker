from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from django.urls import path
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('list/', UserListAPIView.as_view(), name='users_list'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('destroy/<int:pk>/', UserDestroyAPIView.as_view(), name='user_destroy'),
]
