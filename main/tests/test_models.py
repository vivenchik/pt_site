from django.test import TestCase
from main.models import Project


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(project_name='Test Project', project_deadline='2020-01-01')

    def test_project_name_label(self):
        project = Project.objects.get(id=1)
        name = project._meta.get_field('project_name').verbose_name
        self.assertEqual(name, 'project name')

    def test_project_status_label(self):
        project = Project.objects.get(id=1)
        name = project._meta.get_field('project_status').verbose_name
        self.assertEqual(name, 'project status')

    def test_project_deadline_label(self):
        project = Project.objects.get(id=1)
        name = project._meta.get_field('project_deadline').verbose_name
        self.assertEqual(name, 'project deadline')

    def test_team_label(self):
        project = Project.objects.get(id=1)
        name = project._meta.get_field('team').verbose_name
        self.assertEqual(name, 'team')

    def test_project_name_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('project_name').max_length
        self.assertEqual(max_length, 100)

    def test_project_status_verbose(self):  # TODO
        Project.objects.create(project_name='WrongVerbose', project_status=2)
        pass

    def test_str(self):
        project = Project.objects.get(id=1)
        self.assertEqual(project.__str__(), 'Project Test Project on the 0%, deadline is 2020-01-01\n')

