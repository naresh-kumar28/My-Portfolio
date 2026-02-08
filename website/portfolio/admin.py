from django.contrib import admin
from .models import Project, Member, Contact

# Register your models here.
admin.site.register(Project)
admin.site.register(Member)
admin.site.register(Contact)