from django.urls import path, include
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'projects/<str:project_name>/', views.project_page, name='project_page'),
    path(r'projects/', views.projects_list, name='projects_list'),
    path(r'personal/', views.personal, name='personal'),
    path(r'', include('social_django.urls', namespace='social')),
    path(r'logout/', views.logout, name='logout'),
]
