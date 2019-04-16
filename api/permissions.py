from rest_framework.permissions import BasePermission


class IsPrincipal(BasePermission):
    message = "You are not the principal of this School."
    # print("You are not the principal of this School.")
    
    def has_object_permission(self, request, view, obj):
        if obj.principal == request.user:
            return True
        return False

class IsPrincipalDe(BasePermission):
    message = "You are not the principal of this School."

    def has_object_permission(self, request, view, obj):
        if obj.school.principal == request.user:
            return True
        return False