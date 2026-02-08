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
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)