from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    candidate = serializers.ReadOnlyField(
        source="candidate.username"
    )

    job_title = serializers.ReadOnlyField(
        source="job.title"
    )

    class Meta:
        model = Application

        fields = [
            "id",
            "job",
            "job_title",
            "candidate",
            "cover_letter",
            "status",
            "applied_at",
        ]

        read_only_fields = [
            "id",
            "job_title",
            "candidate",
            "status",
            "applied_at",
        ]