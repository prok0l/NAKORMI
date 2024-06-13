from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from django.http import JsonResponse
from rest_framework_api_key.permissions import HasAPIKey

from user.models import Volunteer
from .filters import TransferFilter, ReportFilter, TransferFilterSet, ReportFilterSet
from .models import Tag, Report, Transfer
from .serializers import TagSerializer, ReportSerializer, TransferSerializer

from main.serializers import TgIdSerializer


# Create your views here.


class GetTags(APIView):
    """Получение, создание, редактирование тэгов"""

    permission_classes = [HasAPIKey]

    # TODO переписать на генерики
    @staticmethod
    def get(request, level, *args, **kwargs):
        tags = Tag.objects.filter(level=level)
        return JsonResponse({'tags': TagSerializer(tags, many=True).data})


class ReportView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Получение репорта (фильтрация district, tg_id)"""
    serializer_class = ReportSerializer
    permission_classes = [HasAPIKey]
    filter_backends = [ReportFilter]
    filterset_fields = ['from_user__district', 'from_user', 'to_user']
    filterset_class = ReportFilterSet

    def get_queryset(self):
        user = TgIdSerializer(data=self.request.headers)

        user.is_valid(raise_exception=True)
        if user.data.get('tg_id').is_admin:
            return Report.objects.all()
        else:
            return Report.objects.get(from_user__tg_id=user.data.get('tg_id')) | Report.objects.get(
                to_user__tg_id=user.data.get('tg_id'))


class TransferView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Получение трансфера (фильтрация district, tg_id)"""
    serializer_class = TransferSerializer
    permission_classes = [HasAPIKey]
    filter_backends = [TransferFilter]
    filterset_fields = ['sender_tg_id', 'recipient_tg_id', 'report__from_user__district']
    filterset_class = TransferFilterSet

    def get_queryset(self):
        user = TgIdSerializer(data=self.request.headers)
        queryset = Transfer.objects.all()

        user.is_valid(raise_exception=True)
        if not user.data.get('tg_id').is_admin:
            queryset = (queryset.filter(report__from_user__tg_id=user.data.get('tg_id')) |
                        queryset.filter(report__to_user__tg_id=user.data.get('tg_id')))
        return queryset
