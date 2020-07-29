from django.contrib import admin
from .models import Project, MomentInProject, Profile

admin.site.register(Project)
admin.site.register(Profile)


@admin.register(MomentInProject)
class MomentInProjectAdmin(admin.ModelAdmin):
    list_filter = ('project',)
    ordering = ('sort_key',)
