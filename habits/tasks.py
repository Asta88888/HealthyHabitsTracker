from django.utils import timezone
from celery import shared_task
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task()
def telegram_notification():
    habits = Habit.objects.all()
    current_date = timezone.localtime().time()
    for habit in habits:
        if habit.time <= current_date:
            chat_id = habit.user.tg_chat_id
            message = f"Я буду {habit.action} в {habit.time} в {habit.place}."
            send_telegram_message(chat_id, message)
