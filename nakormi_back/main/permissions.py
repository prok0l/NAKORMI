from rest_framework.permissions import BasePermission, SAFE_METHODS
from user.models import Volunteer

from .serializers import TgIdSerializer


class IsAdminOrReadOnly(BasePermission):
    """Ограничение доступа на создание и редактирование только для админов"""

    def has_permission(self, request, view):
        tg_id = TgIdSerializer(data=request.headers)
        if not tg_id.is_valid():
            return False
        else:
            return bool(request.method in SAFE_METHODS or bool(tg_id.validated_data.get('tg_id').is_admin))

    def has_object_permission(self, request, view, obj):
        tg_id = TgIdSerializer(data=request.headers)
        if not tg_id.is_valid():
            return False
        else:
            return bool(request.method in SAFE_METHODS or bool(tg_id.validated_data.get('tg_id').is_admin))
