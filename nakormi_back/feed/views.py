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
    filterset_fields = ['tg_id', 'tg_id__district']
    filterset_class = ReportFilterSet

    def get_queryset(self):
        user = Volunteer.objects.get(tg_id=self.request.headers.get('Tg-Id'))
        if user.is_admin:
            return Report.objects.all()
        else:
            return Report.objects.get(tg_id=user.tg_id)


class TransferView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Получение трансфера (фильтрация district, tg_id)"""
    serializer_class = TransferSerializer
    permission_classes = [HasAPIKey]
    filter_backends = [TransferFilter]
    filterset_fields = ['report__tg_id__tg_id', 'report__tg_id__district']
    filterset_class = TransferFilterSet

    def get_queryset(self):
        print(self.request.headers.get('Tg-Id'))
        user = Volunteer.objects.get(tg_id=self.request.headers.get('Tg-Id'))
        queryset = Transfer.objects.all()

        if not user.is_admin:
            queryset = queryset.filter(tg_id=user.tg_id)
        return queryset
