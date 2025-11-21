from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer
# Create your views here.



class TaskListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.user.role != "admin":
            return Response({"detail: Only admin can create tasks"}, status = 403)
        
        serializer = TaskSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(serializer.data , status = 201)
        
        return Response(serializer.error , status = 400)
    


class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        task = Task.objects.get(id = pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = Task.objects.get(id = pk)

        if request.user.role != "admin":
            return Response({"detail: Only admin can edit tasks"}, status = 403)
        
        serializer = TaskSerializer(task, data = request.data, partial = True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
       
        return Response(serializer.errors, status = 400)
    
    def delete(self , request, pk):

        task = Task.objects.get(id = pk)
        
        if request.user.role != "admin":
            return Response({"detail: Only admin can edit tasks"}, status = 403)
        
        task.delete()
        Response(status = 204)

        


