from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectMemberView, MyProjectsView, UserProjectsView
)
from tasks.views import AssignTaskToProjectView

urlpatterns = [
    path("", ProjectListView.as_view(), name='project_list'), 
    path("my/", MyProjectsView.as_view(), name='my_projects'),
    path("<uuid:pk>/", ProjectDetailView.as_view(), name='project-detail'), 
    path('<uuid:pk>/members/', ProjectMemberView.as_view(), name='project-members'),
    path('<uuid:pk>/tasks/add/', AssignTaskToProjectView.as_view(), name='assign-task-to-project'),
    path('my/', MyProjectsView.as_view(), name='my-projects'),
    
    # Specific user's projects (admin/manager can view)
    path('user/<uuid:user_id>/', UserProjectsView.as_view(), name='user-projects'),
]