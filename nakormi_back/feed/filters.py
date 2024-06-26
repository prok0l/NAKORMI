import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from feed.models import Transfer, Report


class TransferFilterSet(django_filters.FilterSet):
    class Meta:
        model = Transfer
        fields = {
            'report__from_user__tg_id': ['exact'],
            'report__from_user__district': ['exact'],
            'report__to_user__tg_id': ['exact']
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
            filter_fields['report__from_user__district'] = data['district']
        if 'sender_tg_id' in data:
            filter_fields['report__from_user__tg_id'] = data['sender_tg_id']
        if 'recipient_tg_id' in data:
            filter_fields['report__to_user__tg_id'] = data['recipient_tg_id']

        # Возвращаем инстанс фильтра
        return filterset_class(data=filter_fields, queryset=queryset, request=request)


class ReportFilterSet(django_filters.FilterSet):
    class Meta:
        model = Report
        fields = {
            'from_user__district': ['exact'],
            'from_user': ['exact'],
            'to_user': ['exact'],
            'point':['exact'],
            'point__is_active':['exact']

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
            filter_fields['from_user__district'] = data['district']
        if 'sender_tg_id' in data:
            filter_fields['from_user'] = data['sender_tg_id']
        if 'recipient_tg_id' in data:
            filter_fields['to_user'] = data['recipient_tg_id']
        if 'point' in data: #Фильтр на точку
            filter_fields['point'] = data['point']
        if 'point_is_active' in data: #Фильтр на на активную/удаленную точку
            filter_fields['point__is_active'] = data['point_is_active']

        # Возвращаем инстанс фильтра
        return filterset_class(data=filter_fields, queryset=queryset, request=request)
