from django.contrib import admin
from .models import Project, MyUser, MySmartUser

admin.site.register(Project)
admin.site.register(MyUser)
admin.site.register(MySmartUser)
