from rest_framework.response import Response
from rest_framework import status
from .models import Client_model,Project_model
from .serializer import ClientSerializer,ProjectSerializer,UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_post_clients(request):
    if request.method == 'GET':
        clients = Client_model.objects.all()
        serialized = ClientSerializer(clients, many=True)
        if serialized.data:
            response_data_list = []
            for item in serialized.data:
                user = UserSerializer(User.objects.get(pk=item['created_by']))
                response_data_list.append({
                    'id': item['id'],
                    'client_name': item['client_name'],
                    'created_at': item['created_at'],
                    'created_by': user.data['username'],
                })
            return Response(response_data_list)
        return Response('GET')
    if request.method == 'POST':
        print(request.user)
        serialized = ClientSerializer(data=request.data)
        #response_data = {}
        if serialized.is_valid():
            client = serialized.save(created_by=request.user)
            response_data = {
                'id': client.id,
                'client_name': client.client_name,
                'created_at': client.created_at,
                'created_by': client.created_by.username
            }
            return Response(response_data)
        return Response('Invalid')


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_put_delete_client(request, id):
    client = get_object_or_404(Client_model, pk=id)
    user_serialized = UserSerializer(client.created_by)
    if request.method == 'GET':
        client_serialized = ClientSerializer(client)
        projects_serialized = ProjectSerializer(Project_model.objects.filter(client=client), many=True)
        project_data = []
        for project in projects_serialized.data:
            project_data.append({
                'id': project['id'],
                'project_name': project['project_name']
            })
        if client_serialized.data:
            response_data = {
                    "id": client_serialized.data['id'],
                    "client_name":client_serialized.data['client_name'],
                    "projects": project_data,
                    "created_at": client_serialized.data['created_at'],
                    "updated_at": client_serialized.data['updated_at'],
                    "created_by": user_serialized.data['username'],
            }
            return Response(response_data)
        return Response('does not exist')
    if request.method == 'PUT':
        serialized = ClientSerializer(client, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response('does not exist or invalid')
    if request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_project(request, id):
    client = get_object_or_404(Client_model, pk=id)
    user_ids = [user['id'] for user in request.data['users']]
    request_data = {
        'project_name': request.data['project_name'],
        'client': client.id,
        'user': user_ids,
        'created_by': request.user.id
    }
    serialized = ProjectSerializer(data=request_data)
    if serialized.is_valid():
        serialized.save()
        user_serialized = UserSerializer(User.objects.filter(pk__in=serialized.data['user']), many=True)
        user_list = []
        for user in user_serialized.data:
            user_list.append({
                'id':user['id'],
                'name': user['username']
            })
        response_data = {
            'id': serialized.data['id'],
            'project_name': serialized.data['project_name'],
            'client': serialized.data['client'],
            'users': user_list,
            'created_at': serialized.data['created_at'],
            'created_by': request.user.username,
        }
        return Response(response_data)
    return Response('invalid')


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_projects(request):
    projects = Project_model.objects.filter(user=request.user)
    project_serialized = ProjectSerializer(projects,  many=True)
    response_data = []
    for project in project_serialized.data:
        user = UserSerializer(User.objects.get(pk=project['created_by']))
        response_data.append({
            'id': project['id'],
            'project_name': project['project_name'],
            'created_at': project['created_at'],
            'created_by': user.data['username'],
        })
    return Response(response_data)


