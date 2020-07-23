from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'projects/<str:project_name>/', views.project_page, name='project_page'),
    path(r'projects/', views.projects_list, name='projects_list'),
    path(r'personal/', views.personal, name='personal'),
    path(r'logout/', views.logout, name='logout'),
    url(r'^media/protected/moment_images/(?P<file>.*)/$', views.serve_protected_moment_images, name='serve_protected_moment_images'),
    url(r'^media/protected/music/(?P<file>.*)/$', views.serve_protected_music, name='serve_protected_music'),
]
