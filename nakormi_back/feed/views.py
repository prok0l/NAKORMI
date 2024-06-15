from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from main.models import Photo
from main.serializers import TgIdSerializer
from .filters import TransferFilter, ReportFilter, TransferFilterSet, ReportFilterSet
from .models import Tag, Report, Transfer, ReportPhoto, TransferPhoto
from .serializers import TagSerializer, ReportSerializer, TransferSerializer, ReportPhotoSerializer


# Create your views here.


class GetTags(APIView):
    """Получение, создание, редактирование тэгов"""

    permission_classes = [HasAPIKey]

    # TODO переписать на генерики
    @staticmethod
    def get(request, level, *args, **kwargs):
        tags = Tag.objects.filter(level=level)
        return JsonResponse({'tags': TagSerializer(tags, many=True).data})


class ReportView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Получение репорта (фильтрация district, tg_id)"""
    serializer_class = ReportSerializer
    permission_classes = [HasAPIKey]
    filter_backends = [ReportFilter]
    filterset_fields = ['point','point__is_active','from_user__district', 'from_user', 'to_user']
    filterset_class = ReportFilterSet

    def get_queryset(self):
        user = TgIdSerializer(data=self.request.headers)

        user.is_valid(raise_exception=True)
        if user.validated_data.get('tg_id').is_admin:
            return Report.objects.all()
        else:
            return Report.objects.get(from_user=user.validated_data.get('tg_id')) | Report.objects.get(
                to_user=user.validated_data.get('tg_id'))


class TransferView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Получение трансфера (фильтрация district, tg_id)"""
    serializer_class = TransferSerializer
    permission_classes = [HasAPIKey]
    filter_backends = [TransferFilter]
    filterset_fields = ['report__point','sender_tg_id', 'recipient_tg_id', 'report__from_user__district']
    filterset_class = TransferFilterSet

    def get_queryset(self):
        user = TgIdSerializer(data=self.request.headers)
        queryset = Transfer.objects.all()

        user.is_valid(raise_exception=True)
        if not user.validated_data.get('tg_id').is_admin:
            queryset = (queryset.filter(report__from_user=user.validated_data.get('tg_id')) |
                        queryset.filter(report__to_user=user.validated_data.get('tg_id')))
        return queryset


class ReportPhotoView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ReportPhotoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report']
    lookup_field = 'report'

    def get_queryset(self):
        user = TgIdSerializer(data=self.request.headers)
        user.is_valid(raise_exception=True)
        if user.validated_data.get('tg_id').is_admin:
            queryset = ReportPhoto.objects.all()
        else:
            queryset = ReportPhoto.objects.filter(report=Report.objects.get(pk=user.validated_data.get('tg_id')))

        return queryset

    def create(self, request, *args, **kwargs):
        user = TgIdSerializer(data=self.request.headers)
        user.is_valid()
        report = Report.objects.get(pk=request.data.get('report'))
        from_user = report.from_user
        to_user = report.to_user
        if user.validated_data.get('tg_id') in (from_user, to_user) and not (ReportPhoto.objects.filter(report=report)):
            uploaded_files = self.request.FILES.getlist('photo')
            photo_list = []
            for file in uploaded_files:
                photo = Photo.objects.create(photo=file)
                photo.save()
                photo_list.append(photo)
            serializer = self.get_serializer(data={'report': request.data['report'], 'photo': photo_list})

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(ReportPhoto.objects.filter(report=report), user.validated_data.get('tg_id') == from_user)
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)


class TransferPhotoView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report']
    def get_queryset(self):
        user = TgIdSerializer(data=self.request.headers)
        user.is_valid(raise_exception=True)

        queryset = TransferPhoto.objects.all()
        return queryset
    def create(self, request, *args, **kwargs):
        user = TgIdSerializer(data=self.request.headers)
        user.is_valid()
        report = Transfer.objects.get(pk=request.data.get('report'))
        from_user = report.from_user
        if user.validated_data.get('tg_id') == from_user and not (TransferPhoto.objects.filter(report=report)):
            uploaded_files = self.request.FILES.getlist('photo')
            photo_list = []
            for file in uploaded_files:
                photo = Photo.objects.create(photo=file)
                photo.save()
                photo_list.append(photo)
            serializer = self.get_serializer(data={'transfer': request.data['report'], 'photo': photo_list})

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)


