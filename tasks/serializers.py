from rest_framework import serializers
from .models import Task, User, Project
from accounts.serializer import UserSerializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "display_name", "bio", "role"]


# class TaskSerializer(serializers.ModelSerializer):
#     assigned_to = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), required=False, allow_null=True
#     )
#     created_by = UserSerializer(read_only=True)
#     is_overdue = serializers.ReadOnlyField()

#     class Meta:
#         model = Task
        
#         fields = [
#             "id", "title", "description", "assigned_to", "created_by", "project",
#             "created_at", "due_date", "status", "priority", "comments", "is_overdue"
#         ]
#         extra_kwargs = {
#             "project": {"required": False, "allow_null": True},
#         }


# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ["id", "title", "description", "members"]

from rest_framework import serializers
from .models import Task, User, Project
from accounts.serializer import UserSerializer

class ProjectBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title"]

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    project = ProjectBasicSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()
    assigned_to_details = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "assigned_to", "assigned_to_details", 
            "created_by", "project", "created_at", "due_date", "status", 
            "priority", "comments", "is_overdue"
        ]
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
        }
    
    def get_assigned_to_details(self, obj):
        if obj.assigned_to:
            return UserSerializer(obj.assigned_to). data
        return None

class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    task_count = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 
                 'members', 'task_count', 'tasks']
        read_only_fields = ['created_by', 'created_at']
    
    def get_task_count(self, obj):
        return obj.tasks. count()