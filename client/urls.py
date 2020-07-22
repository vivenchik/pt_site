from django.urls import path, include
from . import views

urlpatterns = [
    path(r'client_project/<str:project_name>/', views.client_project, name='client_project'),
    path(r'client_project/<str:project_name>/login/', views.user_login, name='client_login'),
    path(r'client_project/<str:project_name>/logout/', views.user_logout, name='client_logout'),
]
