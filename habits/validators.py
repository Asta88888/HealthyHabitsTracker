from rest_framework.serializers import ValidationError
from habits.models import Habit


class HabitValidator:
    """
    Валидатор привычки.
    - Нельзя одновременно указывать reward и related_habit
    - duration_sec <= 120
    - 1 <= periodicity_days <= 7
    - Приятная привычка не может иметь reward и related_habit
    - Связанная привычка должна быть приятной
    """
    def __call__(self, *args, attrs):
        is_pleasant = attrs.get('is_pleasant', False)
        related_habit = attrs.get('related_habit', None)
        reward = attrs.get('reward', None)
        duration = attrs.get('time_to_end', None)
        periodicity = attrs.get('periodicity_days', 1)

        if related_habit and reward:
            raise ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение."
            )
        if duration and duration.total_seconds() > 120:
            raise ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд."
            )
        if periodicity < 1 or periodicity > 7:
            raise ValidationError(
                "Периодичность выполнения должна быть от 1 до 7 дней."
            )
        if is_pleasant and (reward or related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                "Связанной привычкой может быть только приятная привычка."
            )
