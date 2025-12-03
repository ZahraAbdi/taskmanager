from django.db import models
import uuid
from accounts.models import User
# Create your models here.

class Project(models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4)
    title = models.CharField(max_length= 30)
    description = models.TextField(blank= True)
    created_at = models.DateTimeField(auto_now_add=True )
    created_by = models.ForeignKey(User, on_delete= models.CASCADE , related_name = 'project_user')
    members = models.ManyToManyField(User, related_name="projects")

    def __str__(self):
        return self.title
