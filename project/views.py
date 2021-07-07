from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from .models import *
from .forms import *

# Create your views here.

def index(request):
    projects = Project.objects.all()
    clients = Client.objects.all()

    total_projects = projects.count()
    completed = projects.filter(status='Done').count()
    progress = projects.filter(status='In Progress').count()

    context = {
        "projects": projects,
        "clients": clients,
        "total_projects": total_projects,
        "completed": completed,
        "progress": progress
    }
    return render(request, 'project/dashboard.html', context)

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

def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'project/project_form.html', context)

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

def deleteProject(request, pk_project):
    project = Project.objects.get(id=pk_project)

    if request.method == 'POST':
        project.delete()
        return redirect('/')


    context = {'project': project}
    return render(request, 'project/delete.html', context)

def createClient(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'project/client_form.html', context)

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

def deleteClient(request, pk_client):
    client = Client.objects.get(id=pk_client)

    if request.method == 'POST':
        client.delete()
        return redirect('/')

    context = {'client': client}
    return render(request, 'project/delete_client.html', context)

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