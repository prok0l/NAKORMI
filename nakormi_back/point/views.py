from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from django.http import JsonResponse

from user.models import Volunteer
from .serializers import ReceptionSerializer


class TakeFeeds(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ReceptionSerializer(data=request.data)

        # user = Volunteer.objects.filter(tg_id=request.data.get('tg_id', None))
        # for feed in request.data.get('content'):
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.errors, safe=False)



