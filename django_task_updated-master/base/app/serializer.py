from rest_framework import serializers
from .models import Client_model,Project_model
from django.contrib.auth.models import User


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_model
        fields = '__all__'
        read_only_fields = ['created_by']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_model
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['id', 'username']
