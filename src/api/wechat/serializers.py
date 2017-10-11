# -- coding: utf-8 --
from rest_framework import serializers

from wechat.models import WechatQR, WechatUser


class WechatQRSerializer(serializers.ModelSerializer):

    class Meta:
        model = WechatQR
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class WechatUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = WechatUser
        fields = '__all__'
