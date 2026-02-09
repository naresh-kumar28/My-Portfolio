from django.contrib import admin
from .models import Project, Member, Contact, Skill

# Register your models here.
admin.site.register(Project)
admin.site.register(Member)
admin.site.register(Contact)
admin.site.register(Skill)