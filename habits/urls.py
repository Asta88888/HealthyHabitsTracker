from django.urls import path, include
from rest_framework.routers import SimpleRouter
from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PublicHabitListAPIView

app_name = HabitsConfig.name

router = SimpleRouter()
router.register('', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('public-habits/', PublicHabitListAPIView.as_view(), name='public-habits'),
]
