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

    # Admin Dashboard Routes
    path('dashboard-x7k/', adminDashboard, name='admin'),
    path('dashboard-x7k/project-add/', projectAdd, name='project-add'),
    path('dashboard-x7k/project-delete/<int:id>/', projectDelete, name='project-delete'),
    path('dashboard-x7k/team-add/', teamAdd, name='team-add'),
    path('dashboard-x7k/team-delete/<int:id>/', teamDelete, name='team-delete'),
    path('dashboard-x7k/add-skill/', addSkill, name='add-skill'),
    path('dashboard-x7k/skill-delete/<int:id>/', skillDelete, name='skill-delete'),
    path('dashboard-x7k/contacts/', adminContacts, name='admin-contacts'),
    path('dashboard-x7k/contact-delete/<int:id>/', contactDelete, name='contact-delete'),

    # Auth Routes
    path('accounts/login/', loginView, name='login'),
    path('accounts/logout/', logoutView, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)