from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/<str:project_name>/', views.project_page, name='project_page'),
    path('projects/', views.projects_list, name='projects_list'),
]
