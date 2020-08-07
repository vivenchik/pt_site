from django.shortcuts import render, get_object_or_404
from .models import Cell, ClientProject, File
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout as dj_logout
import os
from django.http import FileResponse, Http404
import re


def client_project(request, project_name):
    project = get_object_or_404(ClientProject, project_name=project_name)
    if not request.user.is_authenticated or request.user not in project.viewers.all() and not request.user.is_staff:
        return redirect(reverse('client_login', args=[project_name]))

    cells = list(Cell.objects.filter(project__project_name=project_name).order_by('id'))
    wa = ''.join(re.findall(r'\d+', project.contact_whatsapp))
    if wa and wa[0] == '8':
        wa = '7' + wa[1:]
    context = {
        'project_name': project_name,
        'cells': cells,
        'username': request.user.username,
        'telegram': project.contact_telegram,
        'whatsapp': wa,
        'phone': project.contact_phone,
        'email': project.contact_email,
    }
    return render(request, 'client_project.html', context)


def user_login(request, project_name):
    dj_logout(request)
    project = get_object_or_404(ClientProject, project_name=project_name)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect(reverse('client_project', args=[project_name]))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'logo': project.logo if project.logo else None})


def user_logout(request, project_name):
    project = get_object_or_404(ClientProject, project_name=project_name)
    dj_logout(request)
    return redirect(reverse('client_login', args=[project_name]))


def serve_protected_document(request, file):
    document = get_object_or_404(File, file="protected/client_files/" + file).file
    try:
        project = ClientProject.objects.get(cell__files__file=document)
        if not request.user.is_authenticated or request.user not in project.viewers.all() and not request.user.is_staff:
            return redirect(reverse('client_login', args=[project.project_name]))
    except ClientProject.DoesNotExist:
        if not request.user.is_staff:
            raise Http404()

    path, file_name = os.path.split(file)
    response = FileResponse(document.file, )
    response["Content-Disposition"] = "inline; filename=" + file_name
    return response


def serve_document(request, file):
    response = FileResponse(open("media/public/" + file, 'rb'), )
    response["Content-Disposition"] = "inline"
    return response
