from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path(r'client_project/<str:project_name>/', views.client_project, name='client_project'),
    path(r'client_project/<str:project_name>/login/', views.user_login, name='client_login'),
    path(r'client_project/<str:project_name>/logout/', views.user_logout, name='client_logout'),
    url(r'^media/protected/client_files/(?P<file>.*)/$', views.serve_protected_document, name='serve_protected_document'),
]
