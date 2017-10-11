# -- coding: utf-8 --
from rest_framework import serializers

from .models import Tables


class TableSerializer(serializers.ModelSerializer):
    content = serializers.JSONField(source='_content')

    class Meta:
        model = Tables
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')

