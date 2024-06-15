import django_filters

from django_filters.rest_framework import DjangoFilterBackend
from .models import Inventory


class TransferFilterSet(django_filters.FilterSet):
    class Meta:
        model = Inventory
        fields = {
            'tg_id__district__name': ['exact']
        }


class DistrictInventoryFilter(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        # Получаем изначальный фильтрсет
        filterset_class = super().get_filterset_class(view, queryset)
        if not filterset_class:
            return None

        # Создаем объект фильтра с только нужными полями
        data = request.query_params.copy()
        filter_fields = {}
        if 'district' in data:
            filter_fields['tg_id__district__name'] = data['district']
        # Возвращаем инстанс фильтра
        return filterset_class(data=filter_fields, queryset=queryset, request=request)
