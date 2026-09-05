from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.db.models import Q

from .models import Job
from .serializers import JobSerializer


class JobListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        jobs = Job.objects.all().order_by("-created_at")

        search = request.query_params.get("search")

        if search:
            jobs = jobs.filter(
                Q(title__icontains=search)
                | Q(location__icontains=search)
                | Q(skills__icontains=search)
                | Q(description__icontains=search)
            )

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        if request.user.role != "EMPLOYER":
            raise PermissionDenied(
                "Only employers can create jobs."
            )

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(employer=request.user)

            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class JobDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Job.objects.get(pk=pk)

        except Job.DoesNotExist:
            return None

    def get(self, request, pk):

        job = self.get_object(pk)

        if job is None:
            return Response(
                {"detail": "Job not found."},
                status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK)
    

    def put(self, request, pk):

        job = self.get_object(pk)

        if job is None:
            return Response(
                {"detail": "Job not found."},
                status=status.HTTP_404_NOT_FOUND)

        if request.user.role != "EMPLOYER":
            raise PermissionDenied("Only employers can update jobs.")

        if job.employer != request.user:
            raise PermissionDenied("You can only update your own jobs.")

        serializer = JobSerializer(job,data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        job = self.get_object(pk)

        if job is None:
            return Response(
                {"detail": "Job not found."},
                status=status.HTTP_404_NOT_FOUND)

        if request.user.role != "EMPLOYER":
            raise PermissionDenied("Only employers can delete jobs.")


        if job.employer != request.user:
            raise PermissionDenied("You can only delete your own jobs.")

        job.delete()

        return Response(
            {"detail": "Job deleted successfully."},
            status=status.HTTP_204_NO_CONTENT)