# -- coding: utf-8 --
from secrets import token_hex

import logging
import requests
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from common.models import KVObject
from formulas.models import FormulaVarieties, Formula
from model_mixins import CreatedAtMixin, AlphaBaseMixin, UpdatedAtMixin
from varieties.models import VarietiesRecord
from wechat.models import WechatUser

default_logger = logging.getLogger(__name__)


class User(PermissionsMixin, CreatedAtMixin, AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_staff = models.BooleanField(default=False, verbose_name='是员工')
    openid = models.CharField('微信公众号 openid', max_length=30, null=True, unique=True)
    invitation_code = models.CharField('通过哪个邀请码注册', max_length=16, null=True)
    head_img = models.CharField('头像链接', max_length=128, null=True)
    display_name = models.CharField('昵称', max_length=32, null=True)
    introduction = models.CharField('介绍', max_length=128, null=True)

    visit_time = models.BigIntegerField('查看次数', default=0)
    victor_number = models.IntegerField('胜利次数', default=0)
    fail_number = models.IntegerField('失败次数', default=0)
    win_percent = models.DecimalField('胜率', decimal_places=2, max_digits=10, default=0)
    part_number = models.IntegerField('参与次数', default=0)
    ranking = models.IntegerField('排名', null=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        ordering = ('-id',)
        verbose_name = '账号'
        verbose_name_plural = '所有账号列表'
        managed = False

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def masked_username(self):
        if len(self.username) == 11:
            return self.masked_mobile()
        else:
            return '*'*(len(self.username)-1)+self.username[-1]

    def masked_mobile(self):
        tmp = list(self.mobile)
        tmp[3:7] = ['x']*4
        return ''.join(tmp)

    def update_wechat_mobile(self, logger=default_logger):
        """
        从优钱更新手机信息
        """
        try:
            input_params = {'openId': self.openid}
            wechat_main_server_user_object = requests.get(settings.QIAN_GET_WECHAT_USER_INFO_URL, input_params)
            if not wechat_main_server_user_object.json()['success']:
                raise Exception('qian 获取用户信息调用失败，参数 %s，返回 %s' % (input_params, wechat_main_server_user_object.json()))
            mobile = wechat_main_server_user_object.json()['data']['mobile']
            self.mobile = mobile
            self.save()
        except Exception as e:
            logger.error('从 qian 获取用户信息失败: %s' % e.args[0])

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if not InvitationCode.objects.filter(user_id=self.id, default=True).first():
            ic = InvitationCode(
                code=InvitationCode.generate_invitation_code(),
                user_id=self.id,
                limit_count=9999,
                default=True
            )
            ic.save()

    def create_default_subscriptions(self, logger=default_logger):
        """
        创建默认订阅，按品类指定其内置公式
        """
        varieties_code_list = KVObject.objects.filter(k=settings.KV_OBJECT_DEFAULT_VARIETIES_SUBSCRIPTION_KEY).first()
        if not varieties_code_list:
            return
        varieties = VarietiesRecord.objects.filter(
            code__in=list(map(str.strip, varieties_code_list.v.split(',')))
        )
        logger.info('为用户 %s 创建默认订阅: %s' % (self.id, varieties_code_list.v))
        for variety in varieties:
            variety_subscription = VarietiesSubscription(user_id=self.id, varieties_id=variety.id)
            variety_subscription.save()
            formula_ids = FormulaVarieties.objects.filter(varieties_id=variety.id).values_list('formula_id', flat=True)
            formula_subscriptions = [
                FormulaSubscription(
                    user_id=self.id,
                    formula_id=formula.id,
                    varieties_id=variety.id
                ) for formula in Formula.objects.filter(id__in=formula_ids, user_id=None)
            ]
            FormulaSubscription.objects.bulk_create(formula_subscriptions)

    def wechat_info(self):
        return WechatUser.objects.filter(openid=self.openid).first() or WechatUser()

    def send_wechat_template_bind_mobile(self, wechat_client):
        wechat_client.message.send_template(
            self.openid,
            template_id=settings.WECHAT_TEMPLATES['bind_mobile']['id'],
            data={
                'first': {
                    'value': '您的账户还未绑定，请点击绑定'
                },
                'keyword1': {
                    'value': '未绑定'
                },
                'keyword2': {
                    'value': '未绑定'
                },
                'remark': {
                    'value': '请绑定手机号开启预警推送功能。\n\n有色在线人工智能预警会根据目前监控的指标向您每日推送预警信息，也会将通过AI技术进行的行情结果定期发布。更多功能：请访问 %s' % settings.A3_FE_URL
                }
            },
            url=settings.QIAN_MOBILE_VALIDATION_URL % (self.openid, settings.A3_FE_URL),
        )

class FormulaSubscription(AlphaBaseMixin, CreatedAtMixin):
    """
    公式订阅记录
    """
    user_id = models.IntegerField('用户 id')
    formula_id = models.IntegerField('公式 id')
    varieties_id = models.IntegerField('品类 id')

    class Meta:
        db_table = 'user_subscription_formula'
        ordering = ['-id']


class VarietiesSubscription(AlphaBaseMixin, CreatedAtMixin):
    """
    品类订阅记录
    """
    user_id = models.IntegerField('用户 id')
    varieties_id = models.IntegerField('品类 id')

    class Meta:
        db_table = 'user_subscription_varieties'
        ordering = ['-id']


class InvitationCode(AlphaBaseMixin, CreatedAtMixin, UpdatedAtMixin):
    """
    邀请码
    """
    code = models.CharField('邀请码', max_length=8, unique=True)
    user_id = models.IntegerField('创建者用户 id')
    limit_mobile = models.CharField('限制手机号', max_length=11, null=True, blank=True)
    limit_count = models.IntegerField('限制使用次数', default=1, null=True)
    used_at = models.DateTimeField('最后使用时间', null=True)
    used_count = models.IntegerField('已使用了几次', default=0)
    expire_seconds = models.IntegerField('有效时间(秒)', default=3600*24)
    expire_at = models.DateTimeField('过期时间', null=True)
    default = models.BooleanField('是否是默认邀请码', default=True)

    class Meta:
        db_table = 'user_invitation_code'
        ordering = ['-id']
        verbose_name = '邀请码'
        verbose_name_plural = '邀请码'

    @classmethod
    def generate_invitation_code(cls):
        code = token_hex(4)
        while InvitationCode.objects.filter(code=code):
            code = token_hex(4)
        return code

    def save(self, *args, **kwargs):
        if not self.expire_at:
            self.expire_at = self.created_at + timezone.timedelta(seconds=self.expire_seconds)
        if self.limit_mobile:
            self.limit_count = 1
        if InvitationCode.objects.filter(user_id=self.user_id).count():
            self.default = False
        if self.default:
            self.limit_count = 99999
        super(InvitationCode, self).save(*args, **kwargs)

    def user(self):
        return User.objects.filter(id=self.user_id).first()


class UserFeedback(AlphaBaseMixin, CreatedAtMixin):
    content = models.TextField(max_length=1000)
    contact = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'user_feedback'