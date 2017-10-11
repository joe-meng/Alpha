# -- coding: utf-8 --
from rest_framework import serializers

from user.models import FormulaSubscription, VarietiesSubscription, User, InvitationCode, \
    UserFeedback
from wechat.serializers import WechatUserSerializer


class FormulaSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaSubscription
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class VarietiesSubscriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = VarietiesSubscription
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    wechat_info = WechatUserSerializer()

    class Meta:
        model = User
        read_only_fields = ('created_at', )
        exclude = ('password', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'groups', 'user_permissions')


class UserDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'masked_mobile')


class InvitationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvitationCode
        read_only_fields = ('created_at', 'updated_at')
        fields = '__all__'


class InvitationCodeWithUserSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer()

    class Meta:
        model = InvitationCode
        read_only_fields = ('created_at', 'updated_at')
        fields = '__all__'


class UserFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFeedback
        read_only_fields = ('created_at',)
        fields = '__all__'

