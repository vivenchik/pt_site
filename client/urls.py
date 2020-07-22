from django.urls import path, include
from . import views

urlpatterns = [
    path(r'client_project/<str:project_name>/', views.client_project, name='client_project'),
]
