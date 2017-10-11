# encoding: utf-8
from rest_framework import serializers
from .models import Alert, PredictionRecord, AttentionList, QuotesRecords, AiVarieties



class AlertSerializer(serializers.ModelSerializer):
    """预警序列化"""

    class Meta:
        model = Alert
        # fields = ('id', 'title', 'user_id', 'triggered_by', 'is_pushed')
        fields = '__all__'


class PredictionRecordSerializer(serializers.ModelSerializer):
    """预测记录列化"""

    class Meta:
        model = PredictionRecord
        # fields = ('id', 'title', 'user_id', 'triggered_by', 'is_pushed')
        fields = '__all__'


class AttentionListSerializer(serializers.ModelSerializer):
    """关注列表序列化"""

    class Meta:
        model =AttentionList
        # fields = ('id', 'title', 'user_id', 'triggered_by', 'is_pushed')
        fields = '__all__'


class QuotesRecordsSerializer(serializers.ModelSerializer):
    """行情序列化"""

    class Meta:
        model = QuotesRecords
        # fields = ('id', 'title', 'user_id', 'triggered_by', 'is_pushed')
        fields = '__all__'


class AiVarietiesSerializer(serializers.ModelSerializer):
    """品类序列化"""

    class Meta:
        model = AiVarieties
        # fields = ('id', 'title', 'user_id', 'triggered_by', 'is_pushed')
        fields = '__all__'




