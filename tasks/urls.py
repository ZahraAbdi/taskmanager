from django.urls import path
from .views import (
    TaskListView, TaskDetailView, MyTasksView, UserTasksView,
    CommentListCreateView, CommentDetailView
)



urlpatterns = [
    path("", TaskListView.as_view() , name= 'task_list'), 
    path("<uuid:pk>/", TaskDetailView.as_view() , name= 'task-detail'), 
    #path("<uuid:pk>/", TaskStatusUpdateView.as_view(), name = 'update-task')
    path('my/', MyTasksView.as_view(), name='my-tasks'),


    path("<uuid:task_id>/comments/", CommentListCreateView.as_view(), name='task-comments'),
    path("comments/<uuid:pk>/", CommentDetailView.as_view(), name='comment-detail'),
    path('my/', MyTasksView.as_view(), name='my-tasks'),
    path('user/<uuid:user_id>/', UserTasksView.as_view(), name='user-tasks'),
]