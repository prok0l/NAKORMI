from rest_framework.permissions import BasePermission
from user.models import Volunteer


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = Volunteer.objects.filter(pk=request.data.get('tg_id'))
        return bool(
            user and user[0].is_admin
        )