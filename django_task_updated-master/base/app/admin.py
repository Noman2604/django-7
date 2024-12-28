from django.contrib import admin
from .models import Client_model, Project_model


admin.site.register(Client_model)
admin.site.register(Project_model)