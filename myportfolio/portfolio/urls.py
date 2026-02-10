from django.urls import path
from .views import *

#image work
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('project/', project, name='project'),
    path('team/', team, name='team'),

    path('admin/', adminDashboard, name='admin'),
    path('admin/project-add/', projectAdd, name='project-add'),
    path('admin/team-add/', teamAdd, name='team-add'),
    path('admin/add-skill/', addSkill, name='add-skill'),

    #login page work
    path('accounts/login/', loginView, name='login'),
    path('accounts/register/', registerView, name='register'),
    path('accounts/logout/', logoutView, name='logout'),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)