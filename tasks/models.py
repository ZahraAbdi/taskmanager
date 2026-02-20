from django.db import models
from accounts.models import User
from projects.models import Project

from django.utils import timezone
import uuid
# Create your models here.
class Task(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed' , 'Completed'),
        ('canceled' , 'Canceled')
                      )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium' , 'Medium'),
        ('high', 'High' ),
        ('urgent', 'Urgent')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()

    due_date = models.DateTimeField()

    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="pending")

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_tasks",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(
        'projects.Project',  
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )

    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )
    
    #comments = models.TextField(blank= True)


    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"
    

    @property
    def is_overdue(self):
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False



class Comment(models.Model):
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        author = self.author.username if self.author else "unknown"
        return f"Comment by {author} on {self.task.title}"
    



class ActivtiyLog(models.Model):

    id = models.UUIDField(primary_key= True, default= uuid.uuid4 , editable= False)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null = True, related_name= "activity_logs")
    Task= models.ForeignKey(Task, on_delete= models.CASCADE, null = True, blank= True, related_name= "activity_logs")
    project =  models.ForeignKey(Project, on_delete= models.CASCADE, null = True, blank= True, related_name= "activity_logs")
