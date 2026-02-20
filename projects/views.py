from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Project
from .serializers import ProjectSerializer
from accounts.models import User

from tasks.models import Task
from accounts.serializers import UserSerializer

class ProjectListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not (request.user.is_superuser or getattr(request.user, "role", None) == "admin"):
            return Response({"detail": "Only admin can create projects"}, status=403)

        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProjectDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        if not (request.user.is_superuser or getattr(request.user, "role", None) == "admin"):
            return Response({"detail": "Only admin can edit project"}, status=403)

        project = get_object_or_404(Project, id=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not (request.user.is_superuser or getattr(request.user, "role", None) == "admin"):
            return Response({"detail": "Only admin can delete project"}, status=403)

        project = get_object_or_404(Project, id=pk)
        project.delete()
        return Response(status=204)



class ProjectMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        """Get all members of a project"""
        project = get_object_or_404(Project, id=pk)
        
        # Optional: Check if user has access to view members
        # if not (request.user in project.members.all() or request.user.is_superuser or getattr(request.user, "role", None) in ["admin", "manager"]):
        #     return Response({"detail": "You don't have permission to view members"}, status=status.HTTP_403_FORBIDDEN)
        
        members = project.members.all()
        serializer = UserSerializer(members, many=True)
        
        return Response({
            'project_id': project.id,
            'project_name': project.name,
            'member_count': members.count(),
            'members': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Add a member to a project"""
        if not (request.user.is_superuser or getattr(request.user, "role", None) == "admin"):
            return Response(
                {"detail": "Only admin can add members"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        project = get_object_or_404(Project, id=pk)
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {"detail": "user_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)
        
        if user in project.members.all():
            return Response(
                {"detail": "User is already a member"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        project.members.add(user)
        serializer = ProjectSerializer(project, context={'request': request})
        
        return Response({
            'message': f'User {user.email} added to project successfully',
            'project': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Remove a member from a project"""
        if not (request.user.is_superuser or getattr(request.user, "role", None) == "admin"):
            return Response(
                {"detail": "Only admin can remove members"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        project = get_object_or_404(Project, id=pk)
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {"detail": "user_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)
        
        if user not in project.members.all():
            return Response(
                {"detail": "User is not a member of this project"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        project.members.remove(user)
        serializer = ProjectSerializer(project, context={'request': request})
        
        return Response({
            'message': f'User {user.email} removed from project successfully',
            'project': serializer.data
        }, status=status.HTTP_200_OK)


class MyProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = request.user.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    


class UserProjectsView(APIView):
    """Get all projects where a specific user is a member"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None):
        # If no user_id provided, get projects for the logged-in user
        if user_id is None:
            user = request.user
        else:
            # Check permission: users can only view their own projects unless admin/manager
            if str(request.user.id) != str(user_id) and not (
                request.user.is_superuser or getattr(request.user, "role", None) in ["admin", "manager"]
            ):
                return Response(
                    {"detail": "You don't have permission to view this user's projects"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            user = get_object_or_404(User, id=user_id)

        # Get all projects where user is a member
        projects = user.projects.all()

        serializer = ProjectSerializer(projects, many=True, context={'request': request})

        return Response({
            'user_id': str(user.id),
            'user_email': user.email,
            'project_count': projects.count(),
            'projects': serializer.data
        }, status=status.HTTP_200_OK)


class MyProjectsView(APIView):
    """Get all projects for the currently logged-in user"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = request.user.projects.all()
        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        
        return Response({
            'user_id': str(request.user.id),
            'user_email': request.user.email,
            'project_count': projects.count(),
            'projects': serializer.data
        }, status=status.HTTP_200_OK)