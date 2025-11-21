from django.urls import path
from .views import TaskListView, TaskDetailView


urlpatterns = [
    path("tasks/", TaskListView.as_view() , name= 'posts_list'), 
    path("tasks/<uuid:pk>/", TaskDetailView.as_view() , name= 'task-detail'), 
]