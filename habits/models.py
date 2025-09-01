from datetime import timedelta
from django.db import models
from users.models import User


class Habit(models.Model):
    HABIT_FREQUENCY = [
        ("0 * * * *", "каждый час"),
        ("0 */2 * * *", "каждые 2 часа"),
        ("0 */3 * * *", "каждые 3 часа"),
        ("0 9,13,18 * * *", "3 раза в день"),
        ("0 9,18 * * *", "2 раза в день"),
        ("0 9 * * *", "каждый день"),
        ("0 9 */2 * *", "каждые 2 дня"),
        ("0 9 */3 * *", "каждые 3 дня"),
        ("0 9 * * 1,3,5", "выбранные дни"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель привычки', related_name='habits')
    place = models.CharField(max_length=255, verbose_name='Место выполнения привычки')
    time = models.TimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=255, verbose_name='Действие привычки')
    is_pleasant = models.BooleanField(verbose_name='Приятная привычка', default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Связанная привычка', related_name='related_habit')
    frequency = models.CharField(max_length=20, choices=HABIT_FREQUENCY, verbose_name='Периодичность выполнения привычки')
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', blank=True)
    time_to_end = models.DurationField(default=timedelta(seconds=120), verbose_name='Время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='Публичность привычки')
    created_at = models.DateTimeField(auto_now_add=True)
    last_notified_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        time_str = self.time.strftime('%H:%M') if self.time else 'не указано'
        habit_type = 'приятная' if self.is_pleasant else 'полезная'
        return f"Я буду {self.action} в {time_str} в {self.place} ({habit_type} привычка)"
