from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_api_key.permissions import HasAPIKey

from .models import Tag
from .serializers import TagSerializer

# Create your views here.


class GetTags(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def get(request, level, *args, **kwargs):
        tags = Tag.objects.filter(level=level)
        return JsonResponse({'tags': TagSerializer(tags, many=True).data})