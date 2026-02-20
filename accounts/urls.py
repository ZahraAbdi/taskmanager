from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserProfileView,
    ChangePasswordView,
    UsersListView,
    UserTasksView,
    ForgotPasswordView,
    ResetPasswordView
)

urlpatterns = [
    # Authentication
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # User Management
    path('', UsersListView.as_view(), name='users-list'),
    path('users/<uuid:user_id>/tasks/', UserTasksView.as_view(), name='user-tasks'),
]
