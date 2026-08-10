from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Contact, Skill, Certificate

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'image_preview', 'technology', 'created_at')
    search_fields = ('project_name', 'technology', 'project_about')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.display_image_url:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 8px; object-fit: cover;" />', obj.display_image_url)
        return "No Image"
    image_preview.short_description = "Current Image"


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
    list_display = ('title', 'image_preview', 'issuer', 'issue_date', 'created_at')
    search_fields = ('title', 'issuer')
    list_filter = ('created_at',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.display_image_url:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 8px; object-fit: cover;" />', obj.display_image_url)
        return "No Image"
    image_preview.short_description = "Current Image"