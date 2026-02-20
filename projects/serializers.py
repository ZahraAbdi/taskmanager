from rest_framework import serializers
from .models import Project
from accounts.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
   

    # For writing, allow member IDs
    member_ids = serializers.ListField(
        write_only=True, child=serializers.IntegerField(), required=False
    )

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'created_by', 'created_at',
            'members', 'member_count', 'member_ids'
        ]
        read_only_fields = ['created_by', 'created_at', 'members']

    def get_member_count(self, obj):
        return obj.members.count()



    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        project = Project.objects.create(
            **validated_data,
            created_by=self.context['request'].user
        )
        if member_ids:
            project.members.set(member_ids)
        return project

    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if member_ids is not None:
            instance.members.set(member_ids)
        return instance