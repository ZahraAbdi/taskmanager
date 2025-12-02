from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework import  permissions
from .models import Project
from tasks.serializers import ProjectSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.



class ProjectListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many  = True)

        return Response(serializer.data)
    

    def post(self, request):
        
        allowed = (request.user.is_superuser or request.user.role == "admin")
        if not allowed:
            return Response({"detail: Only admin can create project"}, status = 403)
        
        serializer = ProjectSerializer(data =request.data)

        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(data= serializer.data , status = 201)
        
        #print("Serializer Errors:", serializer.errors) 
        return Response(serializer.errors , status  = 400)


class ProjectDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        project = get_object_or_404(Project, id = pk)
        serializer = ProjectSerializer(project)

        return Response(serializer.data)
    
    def put(self, request, pk):
        
        if not request.user.is_superuser and request.user.role != "admin":
            return Response({"detail": "Only admin can edit project"}, status = 403)

        project = get_object_or_404(Project, id = pk)
        serializer = ProjectSerializer(project , data = request.data , partial = True)
      

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors , status = 400)
    

    def delete(self, request , pk):
        permission_classes = [permissions.IsAuthenticated]
        project = get_object_or_404(Project, id = pk)

        if not request.user.is_superuser and request.user.role != "admin":
            return Response({"detail": "Only admin can delete project"}, status = 403)

        project.delete()

        return Response(status = 204)






