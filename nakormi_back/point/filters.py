from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import Point


class PointFilterSet(django_filters.FilterSet):
    class Meta:
        model = Point
        fields = {
            'district__city': ['exact'],
            'district__name': ['exact']
        }


class PointFilter(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        filterset_class = super().get_filterset_class(view, queryset)
        if not filterset_class:
            return None

        data = request.query_params.copy()
        filter_fields = {}
        if request.query_params.get('city'):
            filter_fields['district__city'] = data['city']
        if request.query_params.get('district'):
            filter_fields['district__name'] = data['district']

        # Возвращаем инстанс фильтра
        return filterset_class(data=filter_fields, queryset=queryset, request=request)
