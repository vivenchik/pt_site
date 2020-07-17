from django.test import TestCase
from main.models import Project
from django.urls import reverse
from django.contrib.auth.models import User, Group
import random


class FatherViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_projects = 20
        for project_number in range(1, number_of_projects + 1):
            Project.objects.create(project_name='Project %s' % project_number, project_status=random.uniform(0, 1))
        group = Group.objects.create(name='FREELANCER')
        user = User.objects.create(username='TestUser')
        user.set_password('0000')
        user.groups.add(group)
        user.save()
        Project.objects.get(id=1).team.add(user)
        Project.objects.get(id=10).team.add(user)

    def go_to_page(self, page, args=[]):
        self.client.login(username='TestUser', password='0000')
        resp = self.client.get(reverse(page, args=args), follow=True)
        self.assertEqual(resp.status_code, 200)
        return resp

    def go_to_page_by_url(self, url, with_out_user=False):
        if not with_out_user:
            self.client.login(username='TestUser', password='0000')
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200 if not with_out_user else 400)
        return resp


class ProjectsListViewTest(FatherViewTest):
    def test_view_url_fail_auth(self):
        self.go_to_page_by_url('/projects/', with_out_user=True)

    def test_view_url(self):
        self.go_to_page_by_url('/projects/')

    def test_view_url_by_name(self):
        self.go_to_page('projects_list')

    def test_view_correct_templates(self):
        resp = self.go_to_page('projects_list')
        self.assertTemplateUsed(resp, 'projects_list.html')
        self.assertTemplateUsed(resp, 'base.html')

    def test_context(self):
        resp = self.go_to_page('projects_list')
        self.assertTrue('projects' in resp.context)
        self.assertTrue('my_projects_names' in resp.context)
        self.assertEqual(len(resp.context['projects']), 20)
        self.assertEqual(len(resp.context['my_projects_names']), 2)
        self.assertEqual(resp.context['my_projects_names'], ['Project 1', 'Project 10'])


class ProjectViewTest(FatherViewTest):
    def test_view_url_fail_auth(self):
        self.go_to_page_by_url('/projects/Project%201/', with_out_user=True)

    def test_view_url(self):
        self.go_to_page_by_url('/projects/Project%201/')

    def test_view_url_by_name(self):
        self.go_to_page('project_page', args=['Project 1'])

    def test_wrong_url(self):
        self.client.login(username='TestUser', password='0000')
        resp = self.client.get('/projects/Project/', follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_view_correct_templates(self):
        resp = self.go_to_page('project_page', args=['Project 1'])
        self.assertTemplateUsed(resp, 'project.html')
        self.assertTemplateUsed(resp, 'base.html')

    def test_context(self):
        resp = self.go_to_page('project_page', args=['Project 1'])
        self.assertTrue('team_names' in resp.context)
        self.assertEqual(resp.context['team_names'], ['TestUser'])
        self.assertEqual(resp.context['project'], Project.objects.get(project_name='Project 1'))


class PersonalViewTest(FatherViewTest):
    def test_view_url_fail_auth(self):
        self.go_to_page_by_url('/personal/', with_out_user=True)

    def test_view_url(self):
        self.go_to_page_by_url('/personal/')

    def test_view_url_by_name(self):
        self.go_to_page('personal')

    def test_view_correct_templates(self):
        resp = self.go_to_page('personal')
        self.assertTemplateUsed(resp, 'personal.html')
        self.assertTemplateUsed(resp, 'base.html')

    def test_context(self):
        resp = self.go_to_page('personal')
        self.assertEqual(resp.context['username'], 'TestUser')
        self.assertTrue('first_name' in resp.context)
        self.assertTrue('last_name' in resp.context)
        self.assertTrue('email' in resp.context)
        self.assertEqual(resp.context['groups'], 'FREELANCER')
        self.assertEqual(list(resp.context['projects']), [Project.objects.get(project_name='Project 1'),
                                                          Project.objects.get(project_name='Project 10')])


class IndexViewTest(FatherViewTest):
    def test_view_url_fail_auth(self):
        self.go_to_page_by_url('/', with_out_user=True)

    def test_view_url(self):
        self.go_to_page_by_url('/')

    def test_view_url_by_name(self):
        self.go_to_page('index')

    def test_view_correct_templates(self):
        resp = self.go_to_page('index')
        self.assertTemplateUsed(resp, 'index.html')
        self.assertTemplateUsed(resp, 'base.html')


class LogoutViewTest(FatherViewTest):
    def test_view_url_fail_auth(self):
        self.client.get('/logout/', follow=True)
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 400)

    def test_view_url(self):
        self.client.login(username='TestUser', password='0000')
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)

        self.client.get('/logout/', follow=True)
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 400)

    def test_view_url_by_name(self):
        self.client.login(username='TestUser', password='0000')
        resp = self.client.get(reverse('index'), follow=True)
        self.assertEqual(resp.status_code, 200)

        self.client.get(reverse('logout'), follow=True)
        resp = self.client.get(reverse('index'), follow=True)
        self.assertEqual(resp.status_code, 400)

