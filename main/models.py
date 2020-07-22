from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_status = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    project_deadline = models.DateField(default=timezone.now)

    team = models.ManyToManyField(User, blank=True)
    number_of_moments = models.IntegerField(default=0)

    def safe_save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        number_of_exists_moments = len(MomentInProject.objects.filter(project=self))

        for i in range(number_of_exists_moments, self.number_of_moments):
            MomentInProject.objects.create(sort_key=i, project=self)

    def __str__(self):
        return 'Project {} on the {}%, deadline is {}\n'.format(self.project_name, int(self.project_status * 100),
                                                                self.project_deadline)


class MomentInProject(models.Model):
    sort_key = models.FloatField(default=0)
    header = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    details = models.TextField(max_length=10000, blank=True)

    project = models.ForeignKey(Project, null=True, blank=False, on_delete=models.CASCADE)

    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(default=datetime.now())

    moment_image = models.ImageField(upload_to='moment_images', blank=True)

    STATUS_CHOICES = (
        ('NR', 'Not Ready'),
        ('IP', 'In Progress'),
        ('R', 'Ready'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NR')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.project_status = len(MomentInProject.objects.filter(project=self.project, status='R')) / self.project.number_of_moments
        self.project.safe_save()

    def __str__(self):
        return 'Project {}, Moment {}, {}\n'.format(self.project.project_name, self.sort_key, self.status)
