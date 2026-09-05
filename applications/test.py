from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from jobs.models import Job
from .models import Application


class ApplicationTests(APITestCase):

    def setUp(self):

        self.employer = User.objects.create_user(
            username="employer1",
            email="employer1@yopmail.com",
            password="employer123",
            role="EMPLOYER",
        )

        self.second_employer = User.objects.create_user(
            username="employer2",
            email="employer2@yopmail.com",
            password="employer2123",
            role="EMPLOYER",
        )

        self.candidate = User.objects.create_user(
            username="candidate1",
            email="candidate1@yopmail.com",
            password="candidate123",
            role="CANDIDATE",
        )

        self.job = Job.objects.create(
            employer=self.employer,
            title="Django Developer",
            description="Backend developer",
            location="Delhi",
            skills="Python,Django",
            employment_type="FULL_TIME",
        )

    def test_candidate_can_apply(self):

        self.client.force_authenticate(
            user=self.candidate
        )

        response = self.client.post(
            "/api/applications/",
            {
                "job": self.job.id,
                "cover_letter": "I am interested.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_candidate_cannot_apply_twice(self):

        Application.objects.create(job=self.job,candidate=self.candidate)

        self.client.force_authenticate(user=self.candidate)

        response = self.client.post(
            "/api/applications/",
            {
                "job": self.job.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_employer_can_update_application_status(self):

        application = Application.objects.create(
            job=self.job,
            candidate=self.candidate,
        )

        self.client.force_authenticate(
            user=self.employer
        )

        response = self.client.patch(
            f"/api/applications/{application.id}/",
            {
                "status": "SHORTLISTED",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        application.refresh_from_db()

        self.assertEqual(
            application.status,
            "SHORTLISTED",
        )

    def test_candidate_cannot_update_application_status(self):

        application = Application.objects.create(
            job=self.job,
            candidate=self.candidate,
        )

        self.client.force_authenticate(
            user=self.candidate
        )

        response = self.client.patch(
            f"/api/applications/{application.id}/",
            {
                "status": "HIRED",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )