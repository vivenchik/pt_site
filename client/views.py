from django.shortcuts import render, get_object_or_404
from .models import Cell, ClientProject


def client_project(request, project_name):
    project = get_object_or_404(ClientProject, project_name=project_name)
    cells = list(Cell.objects.filter(project__project_name=project_name).order_by('id'))
    context = {
        'project_name': project_name,
        'cells': cells,
    }
    return render(request, 'client_project.html', context)
