from rest_framework import serializers
from .models import Task, User, Project
from accounts.serializers import UserSerializer
from .models import Task, User, Project
from .models import Task, Comment
from accounts.serializers import UserSerializer
#

class ProjectBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Comment
        fields = ["id", "task", "author", "content", "created_at"]
        read_only_fields = ["author", "created_at"]



class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(), required=False, allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)
    # Show basic project info
    project = ProjectBasicSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "assigned_to", "created_by", "project",
            "created_at", "due_date", "status", "priority", "comments", "is_overdue"
        ]
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
        }        

