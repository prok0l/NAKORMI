from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from .serializers import VolunteerSerializer
from .models import *


class VolunteerView(RetrieveUpdateAPIView):
    permission_classes = [HasAPIKey]

    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        return super().patch(request, *args, **kwargs)
