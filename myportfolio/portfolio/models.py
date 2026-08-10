import os
from django.db import models
from django.core.exceptions import ValidationError

def validate_image_extension(value):
    if not value or not hasattr(value, 'name') or not value.name:
        return
    ext = os.path.splitext(value.name)[1].lower().lstrip('.')
    valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
    if ext and ext not in valid_extensions:
        raise ValidationError(f"File extension '{ext}' is not allowed. Allowed extensions are: {', '.join(valid_extensions)}.")


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
        validators=[validate_image_extension]
    )
    image_url = models.URLField(max_length=500, blank=True, null=True) 

    project_name = models.CharField(max_length=100)
    project_about = models.TextField()
    technology = models.CharField(max_length=200)
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.project_image:
            try:
                url = self.project_image.url
                if url and self.image_url != url:
                    self.image_url = url
                    super().save(update_fields=['image_url'])
            except Exception:
                pass

    @property
    def display_image_url(self):
        if self.project_image:
            try:
                return self.project_image.url
            except Exception:
                pass
        return self.image_url or ''

    def __str__(self):
        return self.project_name


class Certificate(models.Model):
    title = models.CharField(max_length=150)
    issuer = models.CharField(max_length=150)
    certificate_image = models.ImageField(
        upload_to='certificates/',
        blank=True, null=True,
        validators=[validate_image_extension]
    )
    image_url = models.CharField(max_length=500, blank=True, null=True)
    issue_date = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.certificate_image:
            try:
                url = self.certificate_image.url
                if url and self.image_url != url:
                    self.image_url = url
                    super().save(update_fields=['image_url'])
            except Exception:
                pass

    @property
    def display_image_url(self):
        if self.certificate_image:
            try:
                return self.certificate_image.url
            except Exception:
                pass
        return self.image_url or ''

    def __str__(self):
        return f"{self.title} - {self.issuer}"