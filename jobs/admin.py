# from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "employer",
        "location",
        "employment_type",
        "created_at",
    )

    search_fields = (
        "title",
        "location",
        "skills",
    )

    list_filter = (
        "employment_type",
        "location",
    )