from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User
from booking.models import Room


class PostURLTests(TestCase):
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
        cls.url_status = {
            '/unexisting_page': HTTPStatus.NOT_FOUND,
            f'/api/rooms/{cls.room.pk}/book/':
            HTTPStatus.METHOD_NOT_ALLOWED,
            '/api/rooms/': HTTPStatus.OK,
            '/api/mybooking/': HTTPStatus.UNAUTHORIZED,
        }
        cls.urls_authorized = [
            '/api/mybooking/',
        ]
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

    def test_guest_client_direct(self) -> None:
        for address, status in self.url_status.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_authorized_user(self) -> None:
        for url in self.urls_authorized:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
