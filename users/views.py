from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializer import UserSerializer, UserCreateSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserListAPIView(ListAPIView):
    """
    Эндпоинт для получения списка всех пользователей.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Эндпоинт для получения информации о конкретном пользователе.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """
    Эндпоинт для обновления информации о пользователе.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    """
    Эндпоинт для удаления пользователя.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
