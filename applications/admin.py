# from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job",
        "candidate",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "job__title",
        "candidate__username",
        "candidate__email",
    )