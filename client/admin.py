from django.contrib import admin
from .models import Cell, ClientProject, Link, File


@admin.register(Cell)
class ClientProjectAdmin(admin.ModelAdmin):
    list_filter = ('project',)
    ordering = ('id',)


admin.site.register(ClientProject)
admin.site.register(Link)
admin.site.register(File)
