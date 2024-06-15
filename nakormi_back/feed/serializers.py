from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers

from main.models import Photo
from main.serializers import PhotoSerializer
from .models import Tag, Report, Transfer, ReportPhoto

from django.core.files.uploadhandler import FileUploadHandler


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReportActionSerializer(serializers.ModelSerializer):
    content = serializers.ListField()
    photo = serializers.ListField(required=False)

    class Meta:
        model = Report
        fields = '__all__'

    def create(self, validated_data):
        content = validated_data.pop('content')
        instance = self.Meta.model(**validated_data)
        instance.save()
        for cont in content:  # создание transfer, которые прикреплены к report
            transfer_serializer = TransferSerializer(
                data={'report': instance.pk, 'tags': cont.get('tags'), 'volume': cont.get('volume')})
            transfer_serializer.is_valid(raise_exception=True)
            transfer_serializer.save()

        return instance


class TagViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

    def to_representation(self, instance):
        return instance.name


class TransferSerializer(serializers.ModelSerializer):
    tags = TagViewSerializer(many=True, read_only=True)

    class Meta:
        model = Transfer
        fields = '__all__'
        extra_kwargs = {'photo': {'required': False}}


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class MyJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, InMemoryUploadedFile):
            return o.read()


class ReportPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(required=False, write_only=True)
    photo_list = PhotoSerializer(required=False, many = True, read_only=True, queryset = Photo.objects.all())
    class Meta:
        model = ReportPhoto
        fields = '__all__'

    def create(self, validated_data):
        photo = validated_data.pop('photo')
        report = validated_data.pop('report')
        instance = self.Meta.model()

        instance.report = report
        instance.save()
        photo_list = []

        instance.photo.set(photo)
        instance.save()
        return instance


