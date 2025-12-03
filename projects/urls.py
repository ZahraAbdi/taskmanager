from django.urls import path
from .views import ProjectListView, ProjectDetailView
from tasks.views import AssignTaskToProjectView, RemoveTaskFromProjectView

urlpatterns = [
    path("", ProjectListView.as_view() , name= 'project_list'), 
    path("<uuid:pk>/", ProjectDetailView.as_view() , name= 'project-detail'), 
    path("projects/<uuid:project_id>/tasks/add/", AssignTaskToProjectView.as_view(), name="project-task-add"),
    path("projects/<uuid:project_id>/tasks/remove/", RemoveTaskFromProjectView.as_view(), name="project-task-remove"),

]