from django.db import models
from django.contrib.auth.models import User

class Client_model(models.Model):
    client_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name


class Project_model(models.Model):
    project_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField(User, related_name='projects')
    client = models.ForeignKey(Client_model, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name