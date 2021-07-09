import django_filters
from django_filters import CharFilter

from .models import *

class ProjectFilter(django_filters.FilterSet):

    project_name = CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['project_name', 'deadline', 'status']
        exclude = ['name', 'date_created', 'description', 'client']

class ClientFilter(django_filters.FilterSet):
    
    client_name = CharFilter(field_name='name', lookup_expr="icontains")
    
    class Meta:
        model = Client
        fields = ['client_name']