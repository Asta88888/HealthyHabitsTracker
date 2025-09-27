from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@example.com')
        self.other_user = User.objects.create(email='other_user@example.com')
        self.pleasant_habit = Habit.objects.create(
            place='test place',
            time='10:00',
            action='test action',
            is_pleasant=True,
            related_habit=None,
            periodicity_days=1,
            reward='',
            time_to_end='00:05:00',
            is_public=True,
            user=self.user
        )
        self.public_habit = Habit.objects.create(
            place='test place',
            time='10:00',
            action='test action',
            is_pleasant=True,
            related_habit=None,
            periodicity_days=1,
            reward='',
            time_to_end='00:05:00',
            is_public=False,
            user=self.other_user
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create_pleasant(self):
        """Проверка создания привычки полезной"""
        url = reverse('habits:habit-list')
        data = {
            'place': 'park',
            'time': '08:30',
            'action': 'run',
            'is_pleasant': True,
            'periodicity_days': 1,
            'reward': '',
            'related_habit': None,
            'time_to_end': '00:02:00',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(Habit.objects.last().action, 'run')

    def test_habit_create_unpleasant(self):
        """Проверка создания привычки неполезной"""
        url = reverse('habits:habit-list')
        data = {
            'place': 'home',
            'time': '09:30',
            'action': 'lay on sofa',
            'is_pleasant': False,
            'periodicity_days': 1,
            'reward': 'eat chocolate',
            'related_habit': None,
            'time_to_end': '00:02:00',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(Habit.objects.last().action, 'lay on sofa')

    def test_habit_retrieve(self):
        url = reverse("habits:habit-detail", args=(self.pleasant_habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("action"), self.pleasant_habit.action
        )

    def test_public_habit_access(self):
        """Проверка доступа к публичной привычке"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=[self.pleasant_habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update(self):
        """Проверка обновления привычки"""
        url = reverse('habits:habit-detail', args=[self.pleasant_habit.id])

        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'home',
            'time': '09:00',
            'action': 'yoga',
            'is_pleasant': True,
            'periodicity_days': 3,
            'reward': '',
            'related_habit': None,
            'time_to_end': '00:02:00',
            'is_public': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.pleasant_habit.refresh_from_db()
        self.assertEqual(self.pleasant_habit.action, 'yoga')
        self.assertEqual(self.pleasant_habit.place, 'home')
        self.assertFalse(self.pleasant_habit.is_public)

        self.client.force_authenticate(user=self.other_user)
        data['action'] = 'hacking attempt'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_delete(self):
        """Проверка удаления привычки"""
        url = reverse('habits:habit-detail', args=[self.pleasant_habit.id])

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.pleasant_habit.id).exists())

        habit = Habit.objects.create(
            place='office',
            time='12:00',
            action='work',
            is_pleasant=False,
            related_habit=None,
            periodicity_days=1,
            reward='coffee',
            time_to_end=timedelta(seconds=120),
            is_public=False,
            user=self.other_user
        )
        url = reverse('habits:habit-detail', args=[habit.id])

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Habit.objects.filter(id=habit.id).exists())
