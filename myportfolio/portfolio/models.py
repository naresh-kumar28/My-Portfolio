from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class Skill(models.Model):
    skill_name = models.CharField(max_length=100)
    svg_code = models.CharField(max_length=100)

    def __str__(self):
        return self.skill_name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name


class Project(models.Model):
    project_image = models.ImageField(
        upload_to='project/images/',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    image_url = models.URLField(max_length=500, blank=True, null=True) 

    project_name = models.CharField(max_length=100)
    project_about = models.TextField()
    technology = models.CharField(max_length=200)
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def display_image_url(self):
        if self.project_image:
            return self.project_image.url
        return self.image_url or ''

    def __str__(self):
        return self.project_name


class Certificate(models.Model):
    title = models.CharField(max_length=150)
    issuer = models.CharField(max_length=150)
    certificate_image = models.ImageField(
        upload_to='certificates/',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    image_url = models.CharField(max_length=500, blank=True, null=True)
    issue_date = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def display_image_url(self):
        if self.certificate_image:
            return self.certificate_image.url
        return self.image_url or ''

    def __str__(self):
        return f"{self.title} - {self.issuer}"
    