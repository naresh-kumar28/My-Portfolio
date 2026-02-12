from django.shortcuts import render,redirect
from .models import Project, Member, Contact, Skill

#login page
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(req):
    
    return render(req, 'home.html')


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

    if req.method=='POST':
        c = Contact()
        c.name = req.POST.get('name')
        c.email = req.POST.get('email')
        c.contact = req.POST.get('contact')
        c.message = req.POST.get('message')
        c.save()
        return redirect('contact')

    return render(req, 'contact.html')


@login_required
def adminDashboard(req):
    return render(req, 'admin/adminDashboard.html')


@login_required
def projectAdd(req):

    if req.method=='POST':
        p = Project()
        p.project_image = req.FILES.get('project_image')
        p.image_url = req.POST.get('image_url')
        p.project_name = req.POST.get('project_name')
        p.project_about = req.POST.get('project_about')
        p.technology = req.POST.get('technology')
        p.project_url = req.POST.get('project_url')
        p.github_url = req.POST.get('github_url')
        p.save()
        return redirect('project-add')

    return render(req, 'admin/projectAdd.html')


@login_required
def teamAdd(req):

    if req.method=='POST':
        m = Member()
        m.github_avatar_url = req.POST.get('github_avatar_url')
        m.member_name = req.POST.get('member_name')
        m.member_post = req.POST.get('member_post')
        m.about_member = req.POST.get('about_member')
        m.linkedin_url = req.POST.get('linkedin_url')
        m.github_url = req.POST.get('github_url')
        m.save()
        return redirect('team-add')

    return render(req, 'admin/teamAdd.html')

@login_required
def addSkill(req):

    if req.method=='POST':
        s = Skill()
        s.skill_name = req.POST.get('skill_name')
        s.svg_code = req.POST.get('svg_code')
        s.save()
        return redirect('add-skill')

    return render(req, 'admin/add-skills.html')


def loginView(req):

    if req.method=='POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('admin')
        
    return render(req, 'registration/login.html')


def registerView(req):

    if req.method=='POST':
        name = req.POST.get('name')
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = User.objects.create_user(
            first_name=name,
            username=username,
            password=password,
        )
        user.save()
        return redirect('login')

    return render(req, 'registration/register.html')

def logoutView(req):
    logout(req)
    return redirect('login')
    
    