from django.urls import path
from django.contrib.auth.views import auth_login

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'projects/<str:project_name>/', views.project_page, name='project_page'),
    path(r'projects/', views.projects_list, name='projects_list'),
    path(r'login/', views.login, name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'personal/', views.personal, name='personal'),
]
