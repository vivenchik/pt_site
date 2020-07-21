from django.shortcuts import render, get_object_or_404
from .models import Project, MomentInProject
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from .forms import MomentFormDetails, MomentFormImage
from datetime import datetime


def my_login_required(func):
    return login_required(function=func, login_url='/', redirect_field_name='')


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'to_login.html', context={'login_url': settings.LOGIN_URL})
    return render(request, 'index.html')


@my_login_required
def project_page(request, project_name):
    if request.method == 'POST':
        form_det = MomentFormDetails(request.POST)
        form_img = MomentFormImage(request.POST, request.FILES)
        if form_det.is_valid():
            moments = list(MomentInProject.objects.filter(project__project_name=project_name).order_by('sort_key'))
            for moment in moments:  # TODO
                if 'mom%s' % moment.id in request.POST:
                    moment.details += '[{} {}] {}\n'.format(datetime.now().strftime("%b %d %Y %H:%M:%S"),
                                                            request.user, form_det.cleaned_data['details'])
                    moment.save()
        if form_img.is_valid():
            moments = list(MomentInProject.objects.filter(project__project_name=project_name).order_by('sort_key'))
            for moment in moments:  # TODO
                if 'mom%s' % moment.id in request.POST:
                    moment.moment_image = form_img.cleaned_data['image']
                    moment.author = request.user
                    moment.upload_time = datetime.now()
                    moment.status = 'IP'
                    moment.save()

    question = get_object_or_404(Project, project_name=project_name)
    team = Project.objects.get(project_name=project_name).team.all()
    team_names = list(item.username for item in team)
    moments = list(MomentInProject.objects.filter(project__project_name=project_name).order_by('sort_key'))

    form_det = MomentFormDetails()
    form_img = MomentFormImage()

    context = {
        'project': question,
        'team_names': team_names,
        'moments': moments,
        'first_id': moments[0].id,
        'last_id': moments[-1].id,
        'form_det': form_det,
        'form_img': form_img,
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
