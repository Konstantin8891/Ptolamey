from django.test import TestCase

from rest_framework.test import APIClient

from booking.models import Room
from users.models import User


class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        cls.room = Room.objects.create(
            number_or_title='1',
            cost=100,
            population=6
        )
        cls.get_token_url = '/auth/jwt/create'

    def setUp(self) -> None:
        self.guest_client = APIClient()
        response = self.guest_client.post(
            self.get_token_url,
            data={
                'username': self.user.username,
                'password': 'testpassword'
            }
        )
        token = response.json()['access']
        self.authorized_client = APIClient()
        self.authorized_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )

    def test_get_room(self) -> None:
        response = self.guest_client.get('/api/rooms/')
        expectation = [{
            'id': 2,
            'number_or_title': '1',
            'cost': 100.0,
            'population': 6,
            'users': []
        }]
        self.assertEqual(response.json(), expectation)

    def test_post_booking(self) -> None:
        response = self.authorized_client.post(
            f'/api/rooms/{self.room.pk}/book/',
            data={
                "date_start": "2023-09-01",
                "date_end": "2023-09-14"
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.authorized_client.post(
            f'/api/rooms/{self.room.pk}/book/',
            data={
                "date_start": "2023-09-01",
                "date_end": "2023-09-14"
            }
        )
        self.assertEqual(response.status_code, 400)
        response = self.authorized_client.post(
            f'/api/rooms/{self.room.pk}/book/',
            data={
                "date_end": "2023-09-14",
                "date_start": "2023-09-29"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_booking(self) -> None:
        self.authorized_client.post(
            f'/api/rooms/{self.room.pk}/book/',
            data={
                "date_start": "2023-09-01",
                "date_end": "2023-09-14"
            }
        )
        response = self.authorized_client.delete(
            f'/api/rooms/{self.room.pk}/book/',
            data={
                "date_start": "2023-09-01",
                "date_end": "2023-09-14"
            }
        )
        self.assertEqual(response.status_code, 204)
        response = self.authorized_client.delete(
            f'/api/rooms/{self.room.pk}/book/',
            data={
                "date_start": "2023-09-01",
                "date_end": "2023-09-14"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_get_booking(self) -> None:
        response = self.guest_client.get('/api/mybooking/')
        self.assertEqual(response.status_code, 401)
        response = self.authorized_client.get('/api/mybooking/')
        self.assertEqual(response.status_code, 200)
