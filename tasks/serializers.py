from rest_framework import serializers
from .models import Task, User, Project
from accounts.serializer import UserSerializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "display_name", "bio", "role"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Task
        
        fields = [
            "id", "title", "description", "assigned_to", "created_by", "project",
            "created_at", "due_date", "status", "priority", "comments", "is_overdue"
        ]
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
        }


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "members"]

