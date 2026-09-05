# from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

    
class Job(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME= "FULL_TIME", "Full Time"
        PART_TIME = "PART_TIME", "Part Time"
        CONTRACT = "CONTRACT", "Contract"
        INTERNSHIP = "INTERNSHIP", "Internship"


    employer= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="jobs")

    title = models.CharField(max_length=200)

    description = models.TextField()

    location = models.CharField(max_length=200)

    skills = models.TextField(help_text="Comma separated skills")

    employment_type = models.CharField(max_length=20,choices=EmploymentType.choices,default=EmploymentType.FULL_TIME)

    salary = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title