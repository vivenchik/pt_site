from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Icon(models.Model):
    name = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(upload_to='public/icons', blank=True)

    def __str__(self):
        return str(self.name)


class Link(models.Model):
    name = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    icon = models.ForeignKey(Icon, blank=True, null=True, on_delete=models.SET(None))

    def __str__(self):
        return str(self.name)


class File(models.Model):
    name = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='protected/client_files', blank=True)
    icon = models.ForeignKey(Icon, blank=True, null=True, on_delete=models.SET(None))

    def __str__(self):
        return str(self.name)


class ClientProject(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    viewers = models.ManyToManyField(User, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if len(list(Cell.objects.filter(project=self))) == 0:
            Cell.objects.create(cell_name='brief', project=self)
            Cell.objects.create(cell_name='creative', project=self)
            Cell.objects.create(cell_name='contract', project=self)
            Cell.objects.create(cell_name='treatment', project=self)
            Cell.objects.create(cell_name='plan', project=self)
            Cell.objects.create(cell_name='previs', project=self)
            Cell.objects.create(cell_name='draft', project=self)
            Cell.objects.create(cell_name='master', project=self)
            Cell.objects.create(cell_name='assessment', project=self)

    def __str__(self):
        return str(self.project_name)


class Cell(models.Model):
    cell_name = models.CharField(max_length=100, blank=True)
    links = models.ManyToManyField(Link, blank=True)
    files = models.ManyToManyField(File, blank=True)
    info = models.TextField(max_length=10000, blank=True)
    status = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{}::{}, Status:{}%'.format(self.project, self.cell_name, int(self.status * 100))
