from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(email='test@test.ru', password='1234')
        response = self.client.post('/users/token/', {'email': 'test@test.ru', 'password': '1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_habit(self):
        data = {
            'title': 'Test',
            'place': 'Test',
            'lead_time': datetime.fromisoformat('2025-11-03T23:23:23.555555'),
            'action': 'Test',
            'period': 3,
            'time_to_complete': 120,
        }
        response = self.client.post(
            '/habits/habit/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                'id': 5, 'title': 'Test', 'author': 5,
                'place': 'Test', 'lead_time': '2025-11-03T23:23:23.555555+03:00', 'action': 'Test',
                'pleasant_habit': False, 'related_habit': None, 'period': 3,
                'time_to_complete': 120, 'public': False, 'award_habit': [],
                'list_of_pleasant_habits': []
            }
        )

        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_list_habit(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'title': 'Test',
            'place': 'Test',
            'lead_time': datetime.fromisoformat('2025-11-03T23:23:23.555555'),
            'action': 'Test',
            'period': 3,
            'time_to_complete': 120,
        }
        self.client.post(
            '/habits/habit/create/',
            data=data
        )

        response = self.client.get(
            '/habits/habit/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': 8, 'title': 'Test', 'author': 8, 'place': 'Test',
                 'lead_time': '2025-11-03T23:23:23.555555+03:00', 'action': 'Test', 'pleasant_habit': False,
                 'related_habit': None, 'period': 3, 'time_to_complete': 120, 'public': False, 'award_habit': [],
                 'list_of_pleasant_habits': []}]}
        )

    def test_update_habit(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'title': 'Test',
            'place': 'Test',
            'lead_time': datetime.fromisoformat('2025-11-03T23:23:23.555555'),
            'action': 'Test',
            'period': 3,
            'time_to_complete': 120,
        }
        habit = self.client.post(
            '/habits/habit/create/',
            data=data
        )

        response = self.client.patch(
            f'/habits/habit/{habit.json()['id']}/update/',
            data={'period': 4}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 9, 'title': 'Test', 'author': 9,
             'place': 'Test', 'lead_time': '2025-11-03T23:23:23.555555+03:00', 'action': 'Test',
             'pleasant_habit': False, 'related_habit': None, 'period': 4,
             'time_to_complete': 120, 'public': False, 'award_habit': [],
             'list_of_pleasant_habits': []}

        )

    def test_habit_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'title': 'Test',
            'place': 'Test',
            'lead_time': datetime.fromisoformat('2025-11-03T23:23:23.555555'),
            'action': 'Test',
            'period': 3,
            'time_to_complete': 120,
        }
        habit = self.client.post(
            '/habits/habit/create/',
            data=data
        )

        response = self.client.delete(
            f'/habits/habit/{habit.json()['id']}/delete/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_create_habit_for_habit_with_award_habit_award_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'title': 'Test',
            'place': 'Test',
            'lead_time': datetime.fromisoformat('2025-11-03T23:23:23.555555'),
            'action': 'Test',
            'period': 3,
            'time_to_complete': 120,
        }

        habit = self.client.post(
            '/habits/habit/create/',
            data=data
        )

        self.client.post(
            '/habits/award/',
            data={
                'title': 'Test Award',
                'description': 'Test',
                'habit': habit.json()['id']
            },
        )

        data_pleasant = {
            'title': 'Test',
            'place': 'Test',
            'lead_time': datetime.fromisoformat('2025-11-03T23:23:23.555555'),
            'action': 'Test',
            'period': 3,
            'time_to_complete': 120,
            'pleasant_habit': True,
            'related_habit': habit.json()['id'],
        }
        response = self.client.post(
            '/habits/habit/create/',
            data=data_pleasant,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Привязанная обычная привычка уже имеет награды, к ней нельзя привязать приятную привычку.',
                      str(response.data))


# class AwardTestCase(APITestCase):
#
#     def setUp(self) -> None:
#         self.user = User.objects.create_user(email='test@test.ru', password='1234')
#         response = self.client.post('/users/token/', {'email': 'test@test.ru', 'password': '1234'})
#         self.token = response.data['access']
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


class AwardTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя для тестов
        self.user = User.objects.create_user(email='test@test.ru', password='1234')
        response = self.client.post('/users/token/', {'email': 'test@test.ru', 'password': '1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_award_success(self):
        habit = Habit.objects.create(
            author=self.user,
            title='Test Habit',
            place='Test Place',
            lead_time='2025-11-03T23:23:23.555000+03:00',
            action='Test action',
            pleasant_habit=False,
            period=3,
            time_to_complete=120,
            public=False,
        )

        data = {
            'title': 'Award 1',
            'description': 'Описание вознаграждения',
            'habit': habit.id,
        }
        response = self.client.post(
            '/habits/award/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['habit'], habit.id)
        self.assertEqual(response.data['author'], self.user.id)

    def test_create_award_for_pleasant_habit_fail(self):
        pleasant_habit = Habit.objects.create(
            author=self.user,
            title='Pleasant Habit',
            place='Place',
            lead_time='2025-11-03T23:23:23.555000+03:00',
            action='Action Test',
            pleasant_habit=True,
            period=3,
            time_to_complete=60,
            public=False,
        )

        data = {
            'title': 'Award 2',
            'description': 'Описание вознаграждения',
            'habit': pleasant_habit.id,
        }
        response = self.client.post(
            '/habits/award/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Нельзя создавать вознаграждение для приятной привычки.', str(response.data))

    def test_create_award_without_habit_fail(self):
        data = {
            'title': 'Award 3',
            'description': 'Описание вознаграждения',
        }
        response = self.client.post(
            '/habits/award/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('habit', response.json())
        self.assertEqual(response.json()['habit'][0], 'Обязательное поле.')

    def test_create_award_for_habit_with_related_pleasant_habit_fail(self):
        habit = Habit.objects.create(
            author=self.user,
            title='Test Habit',
            place='Test Place',
            lead_time='2025-11-03T23:23:23.555000+03:00',
            action='Test action',
            pleasant_habit=False,
            period=3,
            time_to_complete=120,
            public=False,
        )

        Habit.objects.create(
            author=self.user,
            title='Pleasant Habit',
            place='Place',
            lead_time='2025-11-03T23:23:23.555000+03:00',
            action='Action Test',
            pleasant_habit=True,
            related_habit=habit,
            period=3,
            time_to_complete=60,
            public=False,
        )
        data = {
            'title': 'Award 4',
            'description': 'Описание вознаграждения',
            'habit': habit.id,
        }
        response = self.client.post(
            '/habits/award/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('У привычки с привязанной приятной привычкой нельзя создавать вознаграждение.',
                      str(response.data))
