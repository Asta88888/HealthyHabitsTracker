from datetime import timedelta
from django.db import models
from users.models import User


class Habit(models.Model):
    """
    Модель привычки.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель привычки', related_name='habits')
    place = models.CharField(max_length=255, verbose_name='Место выполнения привычки')
    time = models.TimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=255, verbose_name='Действие привычки')
    is_pleasant = models.BooleanField(verbose_name='Приятная привычка', default=False)
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True,
        null=True, verbose_name='Связанная привычка', related_name='related_habits')
    periodicity_days = models.PositiveSmallIntegerField(
        verbose_name='Периодичность (в днях)', default=1,
        help_text='Количество дней между выполнениями привычки (1–7)')
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', blank=True)
    time_to_end = models.DurationField(default=timedelta(seconds=120), verbose_name='Время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='Публичность привычки')
    created_at = models.DateTimeField(auto_now_add=True)
    last_notified_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        """
        Строковое представление модели привычки.
        """
        time_str = self.time.strftime('%H:%M') if self.time else 'не указано'
        habit_type = 'приятная' if self.is_pleasant else 'полезная'
        return f"Я буду {self.action} в {time_str} в {self.place} ({habit_type} привычка)"
