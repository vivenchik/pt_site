from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Project
from django.http import Http404
from django.template import loader
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required(login_url='/login/google-oauth2/', redirect_field_name='')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/google-oauth2/', redirect_field_name='')
def project_page(request, project_name):
    question = get_object_or_404(Project, project_name=project_name)
    context = {
        'project': question,
    }
    return render(request, 'project.html', context)


@login_required(login_url='/login/google-oauth2/', redirect_field_name='')
def projects_list(request):
    projects = Project.objects.order_by('-project_deadline')
    context = {
        'projects': projects,
    }
    return render(request, 'projects_list.html', context)


def logout(request):
    dj_logout(request)
    return redirect('/')


@login_required(login_url='/login/google-oauth2/', redirect_field_name='')
def personal(request):
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'groups': request.user.groups.all()[0].name if len(request.user.groups.all()) != 0 else '',
    }
    return render(request, 'personal.html', context)