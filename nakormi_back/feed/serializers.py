from rest_framework import serializers

from .models import Tag, Report, Transfer


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
        print(validated_data)
        instance.save()
        for cont in content: #создание transfer, которые прикреплены к report
            transfer_serializer = TransferSerializer(
                data={'report': instance.pk, 'tags': cont.get('tags'), 'volume': cont.get('volume')})
            transfer_serializer.is_valid(raise_exception=True)
            transfer_serializer.save()

        return instance


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
        extra_kwargs = {'photo': {'required': False}}


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

