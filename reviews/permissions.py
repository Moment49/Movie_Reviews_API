from rest_framework.permissions import BasePermission
from rest_framework.validators import ValidationError
from rest_framework import status

class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        if obj.user == request.user:
            return True
        else:
            raise ValidationError({"message":"Sorry!! You can't update or delete a review or comment that is not yours"})

