from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Only admin users have access"""
    message = "Only administrators can access this resource"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrManager(permissions.BasePermission):
    """Admin or Manager users have access"""
    message = "Only administrators or managers can access this resource"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']