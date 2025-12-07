from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectMemberView, MyProjectsView
)
from tasks.views import AssignTaskToProjectView, RemoveTaskFromProjectView

urlpatterns = [
    path("", ProjectListView.as_view(), name='project_list'), 
    path("my/", MyProjectsView.as_view(), name='my_projects'),
    path("<uuid:pk>/", ProjectDetailView.as_view(), name='project-detail'), 
    path("<uuid:pk>/members/", ProjectMemberView.as_view(), name='project-members'),
    path("<uuid:project_id>/tasks/add/", AssignTaskToProjectView.as_view(), name="project-task-add"),
    path("tasks/<uuid:task_id>/remove/", RemoveTaskFromProjectView.as_view(), name="project-task-remove"),
]