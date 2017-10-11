# -- coding: utf-8 --
from rest_framework import serializers

from .models import VarietiesRecord


class VarietiesRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = VarietiesRecord
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class VarietiesRecordSerializerWithSubscription(serializers.ModelSerializer):
    subscribed = serializers.BooleanField(required=False)
    subscription_id = serializers.IntegerField(required=False)
    count = serializers.IntegerField(required=False)

    class Meta:
        model = VarietiesRecord
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')

