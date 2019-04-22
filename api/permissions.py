from rest_framework.permissions import BasePermission


class IsSchoolAdmin(BasePermission):
    message = "You are not the admin  of this School."
    # print("You are not the the admin  of this School.")
    
    def has_object_permission(self, request, view, obj):
        if obj.school_admin == request.user:
            return True
        return False

class IsParent(BasePermission):
    message = "You are not a parent."

    def has_object_permission(self, request, view, obj):
        if obj.parent.user == request.user:
            return True
        return False

     