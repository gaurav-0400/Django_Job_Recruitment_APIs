from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class AuthenticationTests(APITestCase):

    def test_candidate_registration(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "candidate1",
                "email": "candidate1@yopmail.com",
                "password": "candidate123",
                "password_confirm": "candidate123",
                "role": "CANDIDATE",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                username="candidate1"
            ).exists()
        )

    def test_password_mismatch(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "candidate1",
                "email": "candidate1@yopmail.com",
                "password": "candidate123",
                "password_confirm": "wrongpassword",
                "role": "CANDIDATE",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )