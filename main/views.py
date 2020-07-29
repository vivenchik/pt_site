from django.shortcuts import render, get_object_or_404
from .models import Project, MomentInProject, Document
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.conf import settings
from .forms import MomentFormDetails, MomentFormImage, ProfileForm, UserForm, DocumentForm, BooleanCheckForm
import datetime
from django.urls import reverse
from django.http import FileResponse
import os
from django.db import transaction
from django import forms


def group_check(user):
    user_groups = list(group.name for group in list(user.groups.all()))
    in_group = 'FREELANCER' in user_groups or 'EXCLUSIVE' in user_groups or 'INSIDER' in user_groups or user.is_staff
    return in_group and user.profile.user_agreement


def my_user_passes_test_group(func):
    return user_passes_test(group_check, login_url='/', redirect_field_name='')(view_func=func)


def my_login_required(func):
    return login_required(function=func, login_url='/', redirect_field_name='')


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'to_login.html', context={'login_url': settings.LOGIN_URL})
    if not request.user.profile.user_agreement:
        return user_agreement(request)
    if not group_check(request.user):
        dj_logout(request)
        return render(request, 'to_login.html', context={'login_url': settings.LOGIN_URL})
    return render(request, 'index.html')


def user_agreement(request):
    if request.method == 'POST':
        form = BooleanCheckForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['value']:
                request.user.profile.user_agreement = True
                request.user.save()
                return redirect(reverse('index'))
    form = BooleanCheckForm()
    return render(request, 'user_agreement.html', {
        'form': form,
    })


@my_login_required
@my_user_passes_test_group
def project_page(request, project_name):
    project = get_object_or_404(Project, project_name=project_name)
    if request.user not in Project.objects.get(project_name=project_name).team.all():
        return redirect(reverse('projects_list'))
    if request.method == 'POST':
        form_det = MomentFormDetails(request.POST)
        form_img = MomentFormImage(request.POST, request.FILES)
        if form_det.is_valid():
            moments = list(MomentInProject.objects.filter(project__project_name=project_name).order_by('sort_key'))
            for moment in moments:  # TODO
                if 'mom%s' % moment.id in request.POST:
                    moment.details += '[{} {}] {}\n'.format(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"),
                                                            request.user, form_det.cleaned_data['details'])
                    moment.save()
        if form_img.is_valid():
            moments = list(MomentInProject.objects.filter(project__project_name=project_name).order_by('sort_key'))
            for moment in moments:  # TODO
                if 'mom%s' % moment.id in request.POST:
                    moment.moment_image = form_img.cleaned_data['image']
                    moment.author = request.user
                    moment.upload_time = datetime.datetime.now()
                    moment.status = 'IP'
                    moment.save()
        return redirect(reverse('project_page', args=[project_name]))

    team = Project.objects.get(project_name=project_name).team.all()
    team_names = list(item.username for item in team)
    moments = list(MomentInProject.objects.filter(project__project_name=project_name).order_by('sort_key'))

    form_det = MomentFormDetails()
    form_img = MomentFormImage()

    rest_time = datetime.datetime.combine(project.project_deadline, datetime.time(0)) - datetime.datetime.now()
    rest = rest_time.days

    context = {
        'project': project,
        'team_names': team_names,
        'moments': moments,
        'first_id': moments[0].id if moments else 0,  # TODO
        'last_id': moments[-1].id if moments else 0,  # TODO
        'form_det': form_det,
        'form_img': form_img,
        'rest': rest,
    }
    return render(request, 'project.html', context)


@my_login_required
@my_user_passes_test_group
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
@my_user_passes_test_group
def personal(request):
    projects = Project.objects.filter(team__username=request.user.username)
    if request.user.is_staff:
        groups = 'STAFF'
    else:
        groups = ''.join([group.name + ' ' for group in list(request.user.groups.all())])

    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'groups': groups,
        'projects': projects,
        'profile': request.user.profile,
    }
    return render(request, 'personal.html', context)


def logout(request):
    dj_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


@my_login_required
@my_user_passes_test_group
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('personal'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@my_login_required
@my_user_passes_test_group
def documents_page(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            Document.objects.create(user=request.user,
                                    name=form.cleaned_data['name'], file=form.cleaned_data['file'])
        return redirect(reverse('documents_page'))
    else:
        form = DocumentForm()

    documents = list(Document.objects.filter(user=request.user).order_by('-id'))

    context = {
        'documents': documents,
        'form': form,
    }
    return render(request, 'documents_page.html', context)


def serve_protected_file(request, file, document, project):
    if not request.user.is_authenticated or request.user not in project.team.all() and not request.user.is_staff:
        return redirect(reverse('index'))

    path, file_name = os.path.split(file)
    response = FileResponse(document.file, )
    response["Content-Disposition"] = "inline; filename=" + file_name
    return response


def serve_protected_moment_images(request, file):
    document = get_object_or_404(MomentInProject, moment_image="protected/moment_images/" + file).moment_image
    project = MomentInProject.objects.get(moment_image=document).project

    return serve_protected_file(request, file, document, project)


def serve_protected_music(request, file):
    document = get_object_or_404(Project, main_audio="protected/music/" + file).main_audio
    project = Project.objects.get(main_audio=document)

    return serve_protected_file(request, file, document, project)


@my_login_required
def serve_protected_documents(request, file):
    document = get_object_or_404(Document, file="protected/documents/" + file)
    if request.user != document.user and not request.user.is_staff:
        return redirect(reverse('documents_page'))

    path, file_name = os.path.split(file)
    response = FileResponse(document.file.file, )
    response["Content-Disposition"] = "inline; filename=" + file_name
    return response
