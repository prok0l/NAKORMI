from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from feed.models import Transfer, Report
from feed.serializers import ReportActionSerializer
from main.serializers import TgIdSerializer
from main.permissions import IsAdmin
from .serializers import VolunteerSerializer, InventorySerializer, ShareFeedSerializer, UsageFeedSerializer
from .models import *
from .filters import DistrictInventoryFilter


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
        data['is_active'] = True
        return data


class InventoryView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [HasAPIKey]
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tg_id']

    def get_queryset(self):
        user = TgIdSerializer(data=self.request.headers)
        user.is_valid(raise_exception=True)
        queryset = Inventory.objects.filter(tg_id=user.validated_data['tg_id'])
        return queryset


class InventoryAnalytics(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [HasAPIKey, IsAdmin]
    serializer_class = InventorySerializer
    filter_backends = [DistrictInventoryFilter]
    filterset_fields = ['tg_id__district__name']

    def get_queryset(self):
        return Inventory.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        res = dict()
        for item in queryset:
            res[tuple(x.name for x in item.tags.all())] = \
                res.get(tuple(x.name for x in item.tags.all()), 0) + item.volume
        return JsonResponse([{"tags": k, "volume": v} for k, v in res.items()], safe=False, status=status.HTTP_200_OK)


class CheckUserView(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def get(request, pk, *args, **kwargs):
        user = Volunteer.objects.filter(tg_id=pk)
        if user:
            return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)


class ShareFeed(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ShareFeedSerializer(data=request.data)
        user = TgIdSerializer(data=request.headers)
        if not serializer.is_valid() or not user.is_valid():
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        from_user = user.validated_data['tg_id']
        to_user = serializer.validated_data['to_user']

        for feed in serializer.validated_data['content']:
            invent_sender = Inventory.objects.filter(tg_id=from_user,
                                                     tags__in=feed['tags'][:1])
            invent_sender = list(set(x for x in invent_sender if [item.get('id') for item in x.tags.values()] ==
                                     [x.id for x in feed['tags']]))
            if not invent_sender or (invent_sender[0]).volume < feed['volume']:
                return JsonResponse({"error": "excess balance"}, status=status.HTTP_400_BAD_REQUEST)

        for feed in serializer.validated_data['content']:
            invent_sender = Inventory.objects.filter(tg_id=from_user,
                                                     tags__in=feed['tags'][:1])
            invent_sender = list(set(x for x in invent_sender if [item.get('id') for item in x.tags.values()] ==
                                     [x.id for x in feed['tags']]))[0]

            invent_recipient = Inventory.objects.filter(tg_id=to_user,
                                                        tags__in=feed['tags'][:1])
            invent_recipient = list(set(x for x in invent_recipient if [item.get('id') for item in x.tags.values()] ==
                                        [x.id for x in feed['tags']]))
            if invent_recipient:
                invent_recipient = invent_recipient[0]
                invent_recipient.volume = invent_recipient.volume + feed['volume']
            else:
                invent_recipient = Inventory.objects.create(tg_id=to_user,
                                                            volume=feed['volume'])
                for tag in feed['tags']:
                    invent_recipient.tags.add(tag)
            invent_sender.volume = invent_sender.volume - feed['volume']

            invent_sender.save()
            invent_recipient.save()
            if invent_sender.volume == 0:
                invent_sender.delete()

        report_action_serializer = ReportActionSerializer(data=request.data)
        report_action_serializer.is_valid(raise_exception=True)
        obj = report_action_serializer.save()

        return JsonResponse({"id": obj.pk}, status=status.HTTP_200_OK)


class UsageFeedView(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = UsageFeedSerializer(data=request.data)
        user = TgIdSerializer(data=request.headers)
        serializer.is_valid(raise_exception=True)
        user.is_valid(raise_exception=True)

        from_user = user.validated_data['tg_id']

        for feed in serializer.validated_data['content']:
            invent = Inventory.objects.filter(tg_id=from_user,
                                              tags__in=feed['tags'][:1])
            invent = list(set(x for x in invent if [item.get('id') for item in x.tags.values()] ==
                              [x.id for x in feed['tags']]))
            if not invent or (invent := invent[0]).volume < feed['volume']:
                return JsonResponse({"error": "excess balance"}, status=status.HTTP_400_BAD_REQUEST)

        for feed in serializer.validated_data['content']:
            invent = Inventory.objects.filter(tg_id=from_user,
                                              tags__in=feed['tags'][:1])
            invent = list(set(x for x in invent if [item.get('id') for item in x.tags.values()] ==
                              [x.id for x in feed['tags']]))[0]
            invent.volume = invent.volume - feed['volume']
            invent.save()
            if invent.volume == 0:
                invent.delete()

        report_action_serializer = ReportActionSerializer(data=request.data)
        report_action_serializer.is_valid(raise_exception=True)
        obj = report_action_serializer.save()

        return JsonResponse({"id": obj.pk}, status=status.HTTP_200_OK)
