from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from habits.models import Habit
from habits.pagination import StandardResultPagination
from habits.permissions import IsOwner
from habits.serializer import HabitSerializer


class HabitViewSet(ModelViewSet):
    """
    ViewSet для управления привычками пользователя.
    Позволяет создавать, просматривать, обновлять и удалять привычки.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = StandardResultPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ['update', 'list', 'retrieve', 'destroy']:
            self.permission_classes = (IsOwner,)
        return super().get_permissions()


class PublicHabitListAPIView(ListAPIView):
    """
    API для получения списка публичных привычек.
    Только для чтения, с пагинацией.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = StandardResultPagination
