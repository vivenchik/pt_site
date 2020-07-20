from django.contrib import admin
from .models import Project, MomentInProject

admin.site.register(Project)


@admin.register(MomentInProject)
class MomentInProjectAdmin(admin.ModelAdmin):
    list_filter = ('project',)
    ordering = ('sort_key',)
