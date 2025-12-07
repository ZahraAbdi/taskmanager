from rest_framework import serializers
from .models import Project
from accounts.serializer import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 
                 'members', 'member_count']
        read_only_fields = ['created_by', 'created_at']
    
    def get_member_count(self, obj):
        return obj.members.count()