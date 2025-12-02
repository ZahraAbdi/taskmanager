from django.urls import path
from .views import TaskListView, TaskDetailView, MyTasksView, TaskStatusUpdateView



urlpatterns = [
    path("", TaskListView.as_view() , name= 'task_list'), 
    path("<uuid:pk>/", TaskDetailView.as_view() , name= 'task-detail'), 
    path('my/', MyTasksView.as_view(), name='my-tasks'),
]