from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job


class ApplicationListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == "CANDIDATE":

            applications = Application.objects.filter(
                candidate=request.user).select_related("job","candidate").order_by("-applied_at")

        elif request.user.role == "EMPLOYER":

            applications = Application.objects.filter(
                job__employer=request.user
            ).select_related(
                "job",
                "candidate"
            ).order_by("-applied_at")

        else:

            applications = Application.objects.none()

        serializer = ApplicationSerializer(applications,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self, request):
        if request.user.role != "CANDIDATE":
            raise PermissionDenied(
                "Only candidates can apply for jobs."
            )

        job_id = request.data.get("job")

        if not job_id:
            return Response(
                {"job": "Job ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        job = get_object_or_404(
            Job,
            id=job_id
        )

        # Prevent duplicate application
        if Application.objects.filter(
            job=job,
            candidate=request.user
        ).exists():

            return Response(
                {
                    "detail": (
                        "You have already applied "
                        "for this job."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ApplicationSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(candidate=request.user)

            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Application,
            pk=pk
        )

    def get(self, request, pk):

        application = self.get_object(pk)

        # Candidate can see only own application
        if request.user.role == "CANDIDATE":

            if application.candidate != request.user:

                raise PermissionDenied("You can only view your own applications.")

        # Employer can see applications
        # only for their own jobs
        elif request.user.role == "EMPLOYER":

            if application.job.employer != request.user:

                raise PermissionDenied("You cannot view this application.")

        serializer = ApplicationSerializer(application
        )

        return Response(serializer.data,status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        application = self.get_object(pk)

        if request.user.role != "EMPLOYER":

            raise PermissionDenied("Only employers can update application status.")

        if application.job.employer != request.user:

            raise PermissionDenied("You cannot update this application.")

        new_status = request.data.get("status")

        allowed_statuses = [
            Application.Status.APPLIED,
            Application.Status.SHORTLISTED,
            Application.Status.REJECTED,
            Application.Status.HIRED,
        ]

        if new_status not in allowed_statuses:

            return Response(
                {
                    "status": (
                        "Status must be one of: "
                        "APPLIED, SHORTLISTED, "
                        "REJECTED, HIRED."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        serializer = ApplicationSerializer(application)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, pk):

        application = self.get_object(pk)

        if request.user.role != "CANDIDATE":

            raise PermissionDenied("Only candidates can delete applications.")

        if application.candidate != request.user:

            raise PermissionDenied("You can only delete your own application.")

        application.delete()

        return Response(
            {"detail": "Application deleted successfully."},
            status=status.HTTP_204_NO_CONTENT)