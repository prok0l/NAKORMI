from django.forms import model_to_dict
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from django.http import JsonResponse

from feed.serializers import ReportActionSerializer
from user.models import Volunteer, Inventory
from .models import Point
from .serializers import ReceptionSerializer, PointSerializer

from .models import Point
from .map_generater import MapGeneration

from main.permissions import IsAdminOrReadOnly


class TakeFeeds(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ReceptionSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, safe=False)

        for feed in serializer.validated_data['content']:
            invent = Inventory.objects.filter(tg_id=serializer.validated_data['tg_id'],
                                              tags__in=feed['tags'][:1])
            invent = list(set(x for x in invent if [item.get('id') for item in x.tags.values()] ==
                         [x.id for x in feed['tags']]))
            # for tag in feed['tags']:
            #     invent = invent.filter(tags__id=tag.id)
            if invent:
                invent = invent[0]
                invent.volume = invent.volume + feed['volume']
            else:
                invent = Inventory.objects.create(tg_id=serializer.validated_data['tg_id'],
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
    permission_classes = [HasAPIKey, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']
    serializer_class = PointSerializer
    queryset = Point.objects.all()


def get_map(request, *args, **kwargs):
    points = Point.objects.all()
    map_path = MapGeneration(points).map
    return render(request, template_name=map_path)
