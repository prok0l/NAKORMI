from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, viewsets
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from .serializers import VolunteerSerializer, InventorySerializer
from .models import *


class VolunteerView(RetrieveUpdateAPIView):
    """Регистрация пользователя, необходимо указать pk (tg_id) в запросе"""
    permission_classes = [HasAPIKey]

    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

    def patch(self, request, *args, **kwargs):
        data = super().patch(request, *args, **kwargs)
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        data.data['is_active'] = True
        return data

class InventoryView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [HasAPIKey]
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tg_id']
    def get_queryset(self):
        user = Volunteer.objects.get(tg_id=self.request.headers.get('Tg-Id'))
        queryset = Inventory.objects.all()

        if not user.is_admin:
            queryset = queryset.filter(tg_id=user.tg_id)
        return queryset

