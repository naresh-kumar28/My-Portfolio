from django.shortcuts import render,redirect
from .models import Project, Member, Contact, Skill

#login page
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

staff_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='login')


# Create your views here.

def home(req):
    data = {
        'projects': Project.objects.all().order_by('-created_at'),
        'skills': Skill.objects.all(),
        'teams': Member.objects.all(),
    }
    return render(req, 'home.html', data)


def project(req):
    data = {}
    data['projects'] = Project.objects.all().order_by('-created_at')
    return render(req, 'project.html', data)


def about(req):
    data = {}
    data['skills'] = Skill.objects.all()
    return render(req, 'about.html', data)

def team(req):
    data = {}
    data['teams'] = Member.objects.all()
    return render(req, 'team.html', data)


def contact(req):

    if req.method == 'POST':
        c = Contact()
        c.name = req.POST.get('name')
        c.email = req.POST.get('email')
        c.contact = req.POST.get('contact')
        c.message = req.POST.get('message')
        c.save()

        if req.headers.get('HX-Request'):
            return render(req, 'includes/contact_success_partial.html')

        return redirect('contact')

    return render(req, 'contact.html')



@staff_required
def adminDashboard(req):
    context = {
        'project_count': Project.objects.count(),
        'member_count': Member.objects.count(),
        'skill_count': Skill.objects.count(),
        'contact_count': Contact.objects.count(),
        'recent_contacts': Contact.objects.all().order_by('-id')[:5],
        'recent_projects': Project.objects.all().order_by('-id')[:5],
    }
    return render(req, 'admin/adminDashboard.html', context)


@staff_required
def projectAdd(req):
    if req.method == 'POST':
        image = req.FILES.get('project_image')
        if image and image.size > 5 * 1024 * 1024:  # 5MB limit
            projects = Project.objects.all().order_by('-id')
            return render(req, 'admin/projectAdd.html', {'error': 'Image size cannot exceed 5MB.', 'projects': projects})

        p = Project()
        p.project_image = image
        p.image_url = req.POST.get('image_url')
        p.project_name = req.POST.get('project_name')
        p.project_about = req.POST.get('project_about')
        p.technology = req.POST.get('technology')
        p.project_url = req.POST.get('project_url')
        p.github_url = req.POST.get('github_url')
        p.save()
        return redirect('project-add')

    projects = Project.objects.all().order_by('-id')
    return render(req, 'admin/projectAdd.html', {'projects': projects})


@staff_required
def projectDelete(req, id):
    try:
        p = Project.objects.get(id=id)
        p.delete()
    except Project.DoesNotExist:
        pass
    return redirect('project-add')


@staff_required
def teamAdd(req):
    if req.method == 'POST':
        m = Member()
        m.github_avatar_url = req.POST.get('github_avatar_url')
        m.member_name = req.POST.get('member_name')
        m.member_post = req.POST.get('member_post')
        m.about_member = req.POST.get('about_member')
        m.linkedin_url = req.POST.get('linkedin_url')
        m.github_url = req.POST.get('github_url')
        m.save()
        return redirect('team-add')

    teams = Member.objects.all().order_by('-id')
    return render(req, 'admin/teamAdd.html', {'teams': teams})


@staff_required
def teamDelete(req, id):
    try:
        m = Member.objects.get(id=id)
        m.delete()
    except Member.DoesNotExist:
        pass
    return redirect('team-add')


@staff_required
def addSkill(req):
    if req.method == 'POST':
        s = Skill()
        s.skill_name = req.POST.get('skill_name')
        s.svg_code = req.POST.get('svg_code')
        s.save()
        return redirect('add-skill')

    skills = Skill.objects.all().order_by('-id')
    return render(req, 'admin/add-skills.html', {'skills': skills})


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
    contacts = Contact.objects.all().order_by('-id')
    return render(req, 'admin/contacts.html', {'contacts': contacts})


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


def logoutView(req):
    logout(req)
    return redirect('login')

    
    