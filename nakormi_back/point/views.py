from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from django.http import JsonResponse

from user.models import Volunteer, Inventory
from .serializers import ReceptionSerializer


class TakeFeeds(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ReceptionSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, safe=False)

        for feed in serializer.validated_data['content']:
            invent = Inventory.objects.filter(tg_id=serializer.validated_data['tg_id'],
                                              tags__in=feed['tags'])
            for tag in feed['tags']:
                invent = invent.filter(tags__id=tag.id)
            if invent:
                invent = invent[0]
                invent.volume = invent.volume + feed['volume']
            else:
                invent = Inventory.objects.create(tg_id=serializer.validated_data['tg_id'],
                                   volume=feed['volume'])
                for tag in feed['tags']:
                    invent.tags.add(tag)

            invent.save()

        return JsonResponse(serializer.errors, safe=False)



