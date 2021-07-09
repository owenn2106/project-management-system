from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done')
    )

    name = models.CharField(max_length=255, null=True)
    deadline = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, choices=STATUS)

    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name) + " - " + str(self.client)

class Todolist(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done')
    )

    task = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    target_time = models.DateTimeField()
    status = models.CharField(max_length=255, null=True, choices=STATUS)

    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.task) + " - " + str(self.project)