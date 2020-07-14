from django.urls import path
from django.contrib.auth.views import auth_login
from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'projects/<str:project_name>/', views.project_page, name='project_page'),
    path(r'projects/', views.projects_list, name='projects_list'),
    path(r'personal/', views.personal, name='personal'),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', views.logout, name='logout'),
]
