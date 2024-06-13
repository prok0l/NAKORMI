from django.forms import model_to_dict
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from django.http import JsonResponse

from feed.serializers import ReportActionSerializer
from user.models import Volunteer, Inventory, Warehouse
from .models import Point
from .serializers import ReceptionSerializer, PointSerializer

from .models import Point
from .map_generater import MapGeneration

from main.permissions import IsAdminOrReadOnly
from main.serializers import TgIdSerializer
from .filters import PointFilter, PointFilterSet


class TakeFeeds(APIView):
    """Получение корма волонтером с точки"""
    permission_classes = [HasAPIKey]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ReceptionSerializer(data=request.data)
        user = TgIdSerializer(data=request.headers)
        if not serializer.is_valid() or not user.is_valid():
            return JsonResponse(serializer.errors, safe=False)
        for feed in serializer.validated_data['content']:
            invent = Inventory.objects.filter(tg_id=user.validated_data['tg_id'],
                                              tags__in=feed['tags'][:1])
            invent = list(set(x for x in invent if [item.get('id') for item in x.tags.values()] ==
                              [x.id for x in feed['tags']]))
            if invent:
                invent = invent[0]
                invent.volume = invent.volume + feed['volume']
            else:
                invent = Inventory.objects.create(tg_id=user.validated_data['tg_id'],
                                                  volume=feed['volume'])
                for tag in feed['tags']:
                    invent.tags.add(tag)
            report_action_serializer = ReportActionSerializer(data=request.data)
            report_action_serializer.is_valid(raise_exception=True)
            report_action_serializer.save()
            invent.save()

        return JsonResponse(serializer.errors, safe=False)


class PointView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """Получение и создание точек (фильтры city, district)"""
    permission_classes = [HasAPIKey, IsAdminOrReadOnly]
    filter_backends = [PointFilter]
    serializer_class = PointSerializer
    queryset = Point.objects.all()
    filterset_fields = ['district__city', 'district__name']
    filterset_class = PointFilterSet


def get_map(request, *args, **kwargs):
    """Получение карты"""
    # TODO брать точки из Point View, чтобы фильтры работали
    points = Point.objects.all()
    warehouses = Warehouse.objects.all()
    map_path = MapGeneration(points=points, warehouses=warehouses).map
    return render(request, template_name=map_path)
