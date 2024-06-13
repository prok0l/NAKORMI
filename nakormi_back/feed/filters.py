import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from feed.models import Transfer, Report


class TransferFilterSet(django_filters.FilterSet):
    class Meta:
        model = Transfer
        fields = {
            'report__tg_id__tg_id': ['exact'],
            'report__tg_id__district': ['exact'],
        }


class TransferFilter(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        # Получаем изначальный фильтрсет
        filterset_class = super().get_filterset_class(view, queryset)
        if not filterset_class:
            return None

        # Создаем объект фильтра с только нужными полями
        data = request.query_params.copy()
        filter_fields = {}
        if 'district' in data:
            filter_fields['report__tg_id__district'] = data['district']
        if 'tg_id' in data:
            filter_fields['report__tg_id__tg_id'] = data['tg_id']

        # Возвращаем инстанс фильтра
        return filterset_class(data=filter_fields, queryset=queryset, request=request)

class ReportFilterSet(django_filters.FilterSet):
    class Meta:
        model = Report
        fields = {
            'tg_id__district': ['exact'],
            'tg_id': ['exact'],
        }
class ReportFilter(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        # Получаем изначальный фильтрсет
        filterset_class = super().get_filterset_class(view, queryset)
        if not filterset_class:
            return None

        # Создаем объект фильтра с только нужными полями
        data = request.query_params.copy()
        filter_fields = {}
        if 'district' in data:
            filter_fields['tg_id__district'] = data['district']
        if 'tg_id' in data:
            filter_fields['tg_id'] = data['tg_id']

        # Возвращаем инстанс фильтра
        return filterset_class(data=filter_fields, queryset=queryset, request=request)
