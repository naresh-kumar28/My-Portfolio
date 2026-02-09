from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name


class Member(models.Model):
    github_avatar_url = models.URLField()
    member_name = models.CharField(max_length=100)
    member_post = models.CharField(max_length=100)
    about_member = models.CharField(max_length=200)
    linkedin_url = models.URLField()
    github_url = models.URLField()

    def __str__(self):
        return self.member_name


class Project(models.Model):
    project_image = models.ImageField(upload_to='project/images/')
    project_name = models.CharField(max_length=100)
    project_about = models.TextField()
    technology = models.CharField(max_length=200)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.project_name
    