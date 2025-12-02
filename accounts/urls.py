from django.urls import path
from accounts.views import UsersListView
from accounts.views import UserTasksView

urlpatterns = [
    path("", UsersListView.as_view() , name= 'users_list'), 
    path('<uuid:user_id>/tasks/', UserTasksView.as_view(), name='user-tasks'),
    
]