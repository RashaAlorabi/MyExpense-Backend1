from rest_framework.permissions import BasePermission


class IsPrincipal(BasePermission):
    message = "You are not the principal of this School."
    # print("You are not the principal of this School.")
    
    def has_object_permission(self, request, view, obj):
        print("HI--------")
        if obj.principal == request.user:
            print("HI--------")
            return True
        return False