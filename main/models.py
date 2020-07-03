from django.db import models
from django.utils import timezone


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_status = models.FloatField(default=0)
    project_deadline = models.DateField(default=timezone.now)

    def __str__(self):
        return 'Project {} on the {}%, deadline is {}\n'.format(self.project_name, int(self.project_status * 100),
                                                                self.project_deadline)
