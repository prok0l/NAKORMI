from django_filters.rest_framework import DjangoFilterBackend


class PointFilter(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        filters_lst = list()
        if request.query_params.get('city'):
            filters_lst += ['district__city']
        if request.query_params.get('district'):
            filters_lst += ['district__name']
        if filters_lst:
            return filters_lst
        return super().get_filterset(request, queryset, view)
