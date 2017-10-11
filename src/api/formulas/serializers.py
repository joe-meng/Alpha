# -- coding: utf-8 --
from rest_framework import serializers

from formulas.models import Formula, FormulaFunction


class FormulaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Formula
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class FormulaFunctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormulaFunction
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class FormulaSerializerWithSubscription(serializers.ModelSerializer):
    subscribed = serializers.BooleanField(required=False)
    subscription_id = serializers.IntegerField(required=False)

    class Meta:
        model = Formula
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')

