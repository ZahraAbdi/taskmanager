from django.shortcuts import render
from rest_framework import  permissions
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from tasks.serializers import  TaskSerializer
from .serializer import UserSerializer
from tasks.models import Task
from django.shortcuts import get_object_or_404
from accounts.models import User

# Create your views here.

class UsersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = User.objects.all()
        serializer = UserSerializer(projects, many  = True)

        return Response(serializer.data)
    

class UserTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):

        if not (request.user.is_superuser or request.user.role == "admin" or request.user.id == user_id):
            return Response({"detail": "Only admin or the assigned user can see the details of other users taks"}, status=403)
        
        user = get_object_or_404(User, id=user_id)
        tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
