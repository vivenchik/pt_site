from django.shortcuts import render, get_object_or_404
from .models import Project
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings


def my_login_required(func):
    return login_required(function=func, login_url='/', redirect_field_name='')


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'to_login.html', context={'login_url': settings.LOGIN_URL})
    return render(request, 'index.html')


@my_login_required
def project_page(request, project_name):
    question = get_object_or_404(Project, project_name=project_name)
    team = Project.objects.get(project_name=project_name).team.all()
    team_names = list(item.username for item in team)
    context = {
        'project': question,
        'team_names': team_names,
    }
    return render(request, 'project.html', context)


@my_login_required
def projects_list(request):
    projects = Project.objects.order_by('project_deadline')
    my_projects = Project.objects.filter(team__username=request.user.username)
    my_projects_names = list(item.project_name for item in my_projects)
    context = {
        'projects': projects,
        'my_projects_names': my_projects_names,
    }
    return render(request, 'projects_list.html', context)


@my_login_required
def personal(request):
    projects = Project.objects.filter(team__username=request.user.username)
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'groups': request.user.groups.all()[0].name if len(request.user.groups.all()) != 0 else '',  # TODO
        'projects': projects,
    }
    return render(request, 'personal.html', context)


def logout(request):
    dj_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
