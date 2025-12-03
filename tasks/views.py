from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from projects.models import Project
from accounts.models import User


class TaskListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        
        if not request.user.is_superuser and request.user.role != "admin":
            return Response({"detail": "Only admin can create tasks"}, status = 403)
        
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        
        print(serializer.errors)
        return Response(serializer.errors, status=400)
    


class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    # def get(self, request):
    #     tasks = Task.objects.filter(assigned_to = request.user)
    #     serializer = TaskSerializer(tasks, many = True)
    #     return Response(serializer.data)

    
    def put(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        assigned_to_id = request.data.get("assigned_to")

        # Case 1: Normal user self-assigning an unassigned task
        if not (request.user.is_superuser or request.user.role == "admin"):
            if task.assigned_to is None and assigned_to_id == str(request.user.id):
                task.assigned_to = request.user
                task.save()  # Only assign, no other fields updated
                return Response(TaskSerializer(task).data)
            else:
                return Response(
                    {"detail": "Only admin or superuser can edit other fields"},
                    status=403
                )

        # Admin or superuser can self-assign AND edit other fields
        if assigned_to_id == str(request.user.id) or assigned_to_id is None:
            # Allow self-assignment for admin
            task.assigned_to = request.user

        # Update other fields
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    

    # def put(self, request, pk):
    #     task = get_object_or_404(Task, id=pk)

    #     if not (request.user.is_superuser or request.user.role == "admin"):
    #         return Response({"detail": "Only admin can edit tasks"}, status = 403)
        
    #     serializer = TaskSerializer(task, data = request.data, partial = True)
        
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
       
    #     return Response(serializer.errors, status = 400)
    
    def delete(self , request, pk):
        permission_classes = [permissions.IsAuthenticated]
        task = get_object_or_404(Task, id=pk)
        
        if not request.user.is_superuser and request.user.role != "admin":
            return Response({"detail": "Only admin can delte tasks"}, status = 403)
        
        task.delete()
        return Response(status = 204)

class MyTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Make sure user is logged in

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)        


class TaskStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def patch(self, request, pk):
        task = get_object_or_404(Task, id=pk)

        allowed = (request.user.is_superuser 
           or request.user.role == "admin" 
           or task.assigned_to == request.user)

        if task.assigned_to is None:
            return Response({"detail": "Task must be assigned before it can be updated."}, status=403)

        if not allowed:
            return Response({"detail": "Only assigned user or admin can update status"}, status=403)

        status_value = request.data.get("status")
        if status_value not in dict(Task.STATUS_CHOICE):
            return Response({"detail": "Invalid status"}, status=400)

        task.status = status_value
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class AssignTaskToProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        if not (request.user.is_superuser or request.user.role == "admin"):
            return Response({"detail": "Only admin can add task tp project"}, status=403)

        project = get_object_or_404(Project, id=project_id)
        task_id = request.data.get("task_id")
        
        if not task_id:
            return Response({"detail": "task_id is required"}, status=400)

        task = get_object_or_404(Task, id=task_id)

        if task.project and task.project != project:
            return Response(
                {"detail": "Task is already assigned to another project"},
                status=400)

        task.project = project
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    

class RemoveTaskFromProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        if not (request.user.is_superuser or request.user.role == "admin"):
            return Response({"detail": "Only admin can remove tasks"}, status=403)

        task = get_object_or_404(Task, id=task_id)
        task.project = None
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)