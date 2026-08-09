from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Project, Contact, Skill, Certificate
from .forms import ContactForm, ProjectForm, SkillForm, CertificateForm

#login page
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.decorators.http import require_POST

staff_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='login')


# Create your views here.

def home(req):
    data = {
        'projects': Project.objects.all().order_by('-created_at'),
        'skills': Skill.objects.all(),
        'certificates': Certificate.objects.all().order_by('-id'),
    }
    return render(req, 'home.html', data)


def project(req):
    project_list = Project.objects.all().order_by('-created_at')
    paginator = Paginator(project_list, 9)
    page_number = req.GET.get('page')
    projects = paginator.get_page(page_number)
    return render(req, 'project.html', {'projects': projects})


def about(req):
    data = {}
    data['skills'] = Skill.objects.all()
    return render(req, 'about.html', data)


def achievements(req):
    data = {
        'certificates': Certificate.objects.all().order_by('-id'),
    }
    return render(req, 'achievements.html', data)


def contact(req):
    if req.method == 'POST':
        # Honeypot spam check: if filled, request came from an automated bot
        if req.POST.get('website'):
            if req.headers.get('HX-Request'):
                return render(req, 'includes/contact_success_partial.html')
            return redirect('contact')

        form = ContactForm(req.POST)
        if form.is_valid():
            form.save()
            if req.headers.get('HX-Request'):
                return render(req, 'includes/contact_success_partial.html')
            return redirect('contact')
        else:
            return render(req, 'contact.html', {'form': form})

    return render(req, 'contact.html', {'form': ContactForm()})



@staff_required
def adminDashboard(req):
    context = {
        'project_count': Project.objects.count(),
        'certificate_count': Certificate.objects.count(),
        'skill_count': Skill.objects.count(),
        'contact_count': Contact.objects.count(),
        'recent_contacts': Contact.objects.all().order_by('-id')[:5],
        'recent_projects': Project.objects.all().order_by('-id')[:5],
    }
    return render(req, 'admin/adminDashboard.html', context)


@staff_required
def projectAdd(req):
    if req.method == 'POST':
        form = ProjectForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect('project-add')
        else:
            projects = Project.objects.all().order_by('-id')
            return render(req, 'admin/projectAdd.html', {'form': form, 'projects': projects})

    projects = Project.objects.all().order_by('-id')
    return render(req, 'admin/projectAdd.html', {'projects': projects, 'form': ProjectForm()})


@staff_required
def projectDelete(req, id):
    try:
        p = Project.objects.get(id=id)
        p.delete()
    except Project.DoesNotExist:
        pass
    return redirect('project-add')


@staff_required
def addSkill(req):
    if req.method == 'POST':
        form = SkillForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('add-skill')
        else:
            skills = Skill.objects.all().order_by('-id')
            return render(req, 'admin/add-skills.html', {'form': form, 'skills': skills})

    skills = Skill.objects.all().order_by('-id')
    return render(req, 'admin/add-skills.html', {'skills': skills, 'form': SkillForm()})


@staff_required
def skillDelete(req, id):
    try:
        s = Skill.objects.get(id=id)
        s.delete()
    except Skill.DoesNotExist:
        pass
    return redirect('add-skill')


@staff_required
def adminContacts(req):
    contact_list = Contact.objects.all().order_by('-id')
    paginator = Paginator(contact_list, 10)
    page_number = req.GET.get('page')
    contacts = paginator.get_page(page_number)
    return render(req, 'admin/contacts.html', {'contacts': contacts, 'total_count': contact_list.count()})


@staff_required
def contactDelete(req, id):
    try:
        c = Contact.objects.get(id=id)
        c.delete()
    except Contact.DoesNotExist:
        pass
    return redirect('admin-contacts')


def loginView(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('admin')
        else:
            return render(req, 'registration/login.html', {'error': 'Invalid username or password'})
        
    return render(req, 'registration/login.html')


@require_POST
def logoutView(req):
    logout(req)
    return redirect('login')


def robots_txt(req):
    lines = [
        "User-agent: *",
        "Disallow: /dashboard-x7k/",
        "Disallow: /accounts/",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@staff_required
def certificateAdd(req):
    if req.method == 'POST':
        form = CertificateForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect('certificate-add')
        else:
            certificates = Certificate.objects.all().order_by('-id')
            return render(req, 'admin/certificateAdd.html', {'form': form, 'certificates': certificates})

    certificates = Certificate.objects.all().order_by('-id')
    return render(req, 'admin/certificateAdd.html', {'certificates': certificates, 'form': CertificateForm()})


@staff_required
def certificateDelete(req, id):
    try:
        c = Certificate.objects.get(id=id)
        c.delete()
    except Certificate.DoesNotExist:
        pass
    return redirect('certificate-add')

    
    