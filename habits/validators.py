from rest_framework import serializers


def validate_habit(attrs):
    is_pleasant = attrs.get('is_pleasant', False)
    related_habit = attrs.get('related_habit', None)
    reward = attrs.get('reward', None)
    duration = attrs.get('time_to_end', None)
    periodicity = attrs.get('periodicity_days', 1)

    if related_habit and reward:
        raise serializers.ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение."
        )
    if duration and duration.total_seconds() > 120:
        raise serializers.ValidationError(
            "Время выполнения привычки не должно превышать 120 секунд."
        )
    if periodicity < 1 or periodicity > 7:
        raise serializers.ValidationError(
            "Периодичность выполнения должна быть от 1 до 7 дней."
        )
    if is_pleasant and (reward or related_habit):
        raise serializers.ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError(
            "Связанной привычкой может быть только приятная привычка."
        )
