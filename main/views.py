from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Project
from django.http import Http404
from django.template import loader


def index(request):
    return render(request, 'index.html')


def project_page(request, project_name):
    question = get_object_or_404(Project, project_name=project_name)
    context = {
        'project': question,
    }
    return render(request, 'project.html', context)


def projects_list(request):
    projects = Project.objects.order_by('-project_deadline')
    context = {
        'projects': projects,
    }
    return render(request, 'projects_list.html', context)


def login(request):
    return render(request, 'login.html')
