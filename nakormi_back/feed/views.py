from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import mixins,viewsets
from django.http import JsonResponse
from rest_framework_api_key.permissions import HasAPIKey

from user.models import Volunteer
from .models import Tag, Report, Transfer
from .serializers import TagSerializer, ReportSerializer, TransferSerializer


# Create your views here.


class GetTags(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def get(request, level, *args, **kwargs):
        tags = Tag.objects.filter(level=level)
        return JsonResponse({'tags': TagSerializer(tags, many=True).data})



class ReportView(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ReportSerializer
    permission_classes = [HasAPIKey]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tg_id']
    def get_queryset(self):
        user =  Volunteer.objects.get(tg_id =self.request.data.get(['tg_id'][0]))
        if user.is_admin:
            return  Report.objects.all()
        else:
            return Report.objects.get(tg_id = user.tg_id)

class TransferView(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TransferSerializer
    permission_classes = [HasAPIKey]
    def get_queryset(self):
        print(self.request.data)
        user = Volunteer.objects.get(tg_id =self.request.data.get(['tg_id'][0]))
        if user.is_admin:
            return Transfer.objects.all()
        else:
            return Transfer.objects.get(tg_id=user.tg_id)
