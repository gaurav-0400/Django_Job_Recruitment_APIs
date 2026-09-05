from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from .models import Job


class JobTests(APITestCase):

    def setUp(self):
        self.employer = User.objects.create_user(
            username="employer",
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
            username="candidate2",
            email="candidate2@yopmail.com",
            password="candidate2123",
            role="CANDIDATE",
        )

        self.job = Job.objects.create(
            employer=self.employer,
            title="Django Developer",
            description="Backend developer",
            location="Chandigarh",
            skills="Python,Django,PostgreSQL",
            employment_type="FULL_TIME",
            salary=70000,
        )

    def test_employer_can_create_job(self):

        self.client.force_authenticate(
            user=self.employer
        )

        response = self.client.post(
            "/api/jobs/",
            {
                "title": "Python Developer",
                "description": "Backend developer",
                "location": "Delhi",
                "skills": "Python,Flask",
                "employment_type": "FULL_TIME",
                "salary": "80000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_candidate_cannot_create_job(self):

        self.client.force_authenticate(
            user=self.candidate
        )

        response = self.client.post(
            "/api/jobs/",
            {
                "title": "Python Developer",
                "description": "Backend developer",
                "location": "Delhi",
                "skills": "Python,Flask",
                "employment_type": "FULL_TIME",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_candidate_can_view_jobs(self):

        self.client.force_authenticate(
            user=self.candidate
        )

        response = self.client.get(
            "/api/jobs/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_other_employer_cannot_update_job(self):

        self.client.force_authenticate(
            user=self.second_employer
        )

        response = self.client.put(
            f"/api/jobs/{self.job.id}/",
            {
                "title": "Updated Job",
                "description": "Updated description",
                "location": "Mumbai",
                "skills": "Python",
                "employment_type": "FULL_TIME",
                "salary": "90000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )