from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'place', 'time', 'action', 'is_pleasant',
        'related_habit', 'reward', 'periodicity_days', 'time_to_end',
        'is_public', 'created_at', 'last_notified_on',
    )
    search_fields = ('user', 'place', 'action',)
    list_filter = ('user',)
