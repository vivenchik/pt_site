from django.db import models
from django.utils import timezone


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_status = models.FloatField(default=0)
    project_deadline = models.DateField(default=timezone.now)
