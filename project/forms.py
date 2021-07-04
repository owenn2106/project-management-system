from django.forms import ModelForm
from .models import Client, Project, Todolist

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class TodoForm(ModelForm):
    class Meta:
        model = Todolist
        fields='__all__'