from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.index, name='home'),
    path('client/<str:pk_client>/', views.client, name='client'),
    path('details/<str:pk_project>/', views.details, name='project'),

    path('create_project/', views.createProject, name='create_project'),
    path('update_project/<str:pk_project>/', views.updateProject, name='update_project'),
    path('delete_project/<str:pk_project>/', views.deleteProject, name='delete_project'),

    path('create_client/', views.createClient, name='create_client'),
    path('update_client/<str:pk_client>/', views.updateClient, name='update_client'),
    path('delete_client/<str:pk_client>/', views.deleteClient, name='delete_client'),

    path('create_task/<str:pk_project>', views.createTask, name='create_task'),
    path('update_task/<str:pk_task>', views.updateTask, name='update_task'),
    path('delete_task/<str:pk_task>', views.deleteTask, name='delete_task')
]