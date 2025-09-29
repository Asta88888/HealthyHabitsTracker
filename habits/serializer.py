from rest_framework import serializers
from habits.models import Habit
from habits.validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, attrs):
        validate_habit(attrs)
        return attrs
