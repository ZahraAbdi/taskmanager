from django.shortcuts import render
from rest_framework. views import APIView
from rest_framework import permissions
from . models import Project
from .serializers import ProjectSerializer  
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import User

class ProjectListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = Project.objects. all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        allowed = (request.user.is_superuser or request.user.role == "admin")
        if not allowed:
            return Response({"detail": "Only admin can create project"}, status=403) 
        
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(data=serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

class ProjectDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        if not request.user.is_superuser and request.user. role != "admin":
            return Response({"detail": "Only admin can edit project"}, status=403)

        project = get_object_or_404(Project, id=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer. data)
        
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        if not request.user.is_superuser and request.user. role != "admin":
            return Response({"detail": "Only admin can delete project"}, status=403)

        project = get_object_or_404(Project, id=pk)
        project.delete()
        return Response(status=204)

# NEW: Add/Remove users to/from projects
class ProjectMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Add user to project"""
        if not request.user.is_superuser and request.user.role != "admin":
            return Response({"detail": "Only admin can add members"}, status=403)
        
        project = get_object_or_404(Project, id=pk)
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"detail": "user_id is required"}, status=400)
        
        user = get_object_or_404(User, id=user_id)
        
        if user in project.members.all():
            return Response({"detail": "User is already a member"}, status=400)
        
        project. members.add(user)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """Remove user from project"""
        if not request.user.is_superuser and request.user.role != "admin":
            return Response({"detail": "Only admin can remove members"}, status=403)
        
        project = get_object_or_404(Project, id=pk)
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"detail": "user_id is required"}, status=400)
        
        user = get_object_or_404(User, id=user_id)
        project.members.remove(user)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class MyProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get projects where user is a member"""
        projects = request.user.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)