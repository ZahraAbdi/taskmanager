from django.db import models
import uuid
from accounts.models import User

# Create your models here.


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  # added name field
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    members = models.ManyToManyField(User, related_name='projects', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

