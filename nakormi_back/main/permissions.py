from rest_framework.permissions import BasePermission, SAFE_METHODS
from user.models import Volunteer


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        tg_id = request.data.get('tg_id')

        user = Volunteer.objects.get(pk=tg_id)
        return bool(request.method in SAFE_METHODS or bool(user.is_admin))
    def has_object_permission(self, request, view, obj):
        tg_id = request.data.get('tg_id')
        user = Volunteer.objects.get(pk=tg_id)
        return bool(user.is_admin)
