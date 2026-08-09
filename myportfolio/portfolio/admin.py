from django.contrib import admin
from .models import Project, Contact, Skill, Certificate

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'technology', 'created_at')
    search_fields = ('project_name', 'technology', 'project_about')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact')
    search_fields = ('name', 'email', 'message')




@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'svg_code')
    search_fields = ('skill_name',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'issue_date', 'created_at')
    search_fields = ('title', 'issuer')
    list_filter = ('created_at',)