from project.decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .filters import *
from .decorators import *

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, f'Hi {username}, Welcome to SuperProject!')
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'project/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'project/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def index(request):
    projects = Project.objects.all()
    clients = Client.objects.all()

    total_projects = projects.count()
    completed = projects.filter(status='Done').count()
    progress = projects.filter(status='In Progress').count()

    projectFilter = ProjectFilter(request.GET, queryset=projects)
    projects = projectFilter.qs

    clientFilter = ClientFilter(request.GET, queryset=clients)
    clients = clientFilter.qs

    context = {
        "projects": projects,
        "clients": clients,
        "total_projects": total_projects,
        "completed": completed,
        "progress": progress,
        "projectFilter": projectFilter,
        "clientFilter": clientFilter
    }
    return render(request, 'project/dashboard.html', context)

@login_required(login_url='login')
def client(request, pk_client):
    client = Client.objects.get(id=pk_client)
    projects = client.project_set.all()

    total_projects = projects.count()

    context = {
        "projects": projects,
        "client": client,
        "total_projects": total_projects
    }
    return render(request, 'project/client.html', context)

@login_required(login_url='login')
def details(request, pk_project):
    project = Project.objects.get(id=pk_project)
    client = project.client
    todolist = project.todolist_set.all()

    context = {
        "project": project,
        "client": client,
        "todolist": todolist
    }
    return render(request, 'project/details.html', context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'project/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk_project):
    project = Project.objects.get(id=pk_project)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'project/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk_project):
    project = Project.objects.get(id=pk_project)

    if request.method == 'POST':
        project.delete()
        return redirect('/')


    context = {'project': project}
    return render(request, 'project/delete.html', context)

@login_required(login_url='login')
def createClient(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'project/client_form.html', context)

@login_required(login_url='login')
def updateClient(request, pk_client):
    client = Client.objects.get(id=pk_client)
    form = ClientForm(instance=client)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'project/client_form.html', context)

@login_required(login_url='login')
def deleteClient(request, pk_client):
    client = Client.objects.get(id=pk_client)

    if request.method == 'POST':
        client.delete()
        return redirect('/')

    context = {'client': client}
    return render(request, 'project/delete_client.html', context)

@login_required(login_url='login')
def createTask(request, pk_project):
    TaskFormSet = inlineformset_factory(Project, Todolist, fields=('task', 'target_time', 'status'))
    project = Project.objects.get(id=pk_project)
    formset = TaskFormSet(queryset=Todolist.objects.none(), instance=project)

    if request.method == 'POST':
        formset = TaskFormSet(request.POST, instance=project)
        if formset.is_valid():
            formset.save()
            return redirect('../details/' +str(pk_project)) 

    context = {
        'formset': formset, 
        'project': project
    }
    return render(request, 'project/todo_form.html', context)

@login_required(login_url='login')
def updateTask(request, pk_task):
    task = Todolist.objects.get(id=pk_task)
    form = TodoForm(instance=task)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'project/client_form.html', context)

@login_required(login_url='login')
def deleteTask(request, pk_task):
    task = Todolist.objects.get(id=pk_task)

    if request.method == 'POST':
        task.delete()
        return redirect('/')

    context = {'task': task}
    return render(request, 'project/delete_task.html', context)