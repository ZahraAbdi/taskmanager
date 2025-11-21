from django.db import models
from accounts.models import User
from datetime import timezone
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
    title = models.CharField(max_length= 50)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete= models.CASCADE, related_name='user_task')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'created_user')
    created_at = models.DateTimeField(auto_now_add=True )
    due_date = models.DateTimeField(blank= True , null = True)
    status = models.CharField(choices= STATUS_CHOICE , default= 'pending', max_length=15)
    priority = models.CharField(choices = PRIORITY_CHOICES , default = 'medium',  max_length=10 )
    comments = models.TextField(blank= True , null= True)


    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"
    

    @property
    def is_overdue(self):
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False
