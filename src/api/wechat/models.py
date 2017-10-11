from django.db import models
from django.utils import timezone

from enums import WechatSexTypes, WechatQRCodeActionNameTypes, WechatQRScanResultCode
from model_mixins import CreatedAtMixin, AlphaBaseMixin


class WechatUser(CreatedAtMixin, AlphaBaseMixin):
    openid = models.CharField('微信公众号 openid', max_length=32)
    subscribe = models.BooleanField('是否订阅', default=False)
    nickname = models.CharField('微信昵称', max_length=64, null=True)
    sex = models.SmallIntegerField('性别', choices=WechatSexTypes.choices(), null=True)
    language = models.CharField('语言', null=True, max_length=32)
    city = models.CharField('城市', null=True, max_length=32)
    province = models.CharField('省份', null=True, max_length=32)
    country = models.CharField('国家', null=True, max_length=32)
    headimgurl = models.CharField('头像地址', null=True, max_length=256)
    subscribe_time = models.IntegerField('订阅时间', null=True)
    unionid = models.CharField('union id', null=True, max_length=32)
    remark = models.CharField('备注', null=True, max_length=128)
    privilege = models.CharField(null=True, max_length=128)
    groupid = models.IntegerField('组id', null=True)
    tagid_list = models.CharField('tag 列表', null=True, max_length=128)

    class Meta:
        db_table = 'wechat_user'
        ordering = ['-id']


class WechatQR(AlphaBaseMixin, CreatedAtMixin):
    scene_str = models.CharField('scene_str', max_length=64, primary_key=True)
    expire_seconds = models.IntegerField('持续时间，秒为单位', default=3600)
    ticket = models.CharField('ticket', max_length=128, null=True)
    url = models.CharField('url', max_length=256, null=True)
    action_name = models.CharField('action_name', choices=WechatQRCodeActionNameTypes.choices(), max_length=16)
    openid = models.CharField('openid', max_length=32, null=True, unique=True)
    image_url = models.CharField('image_url', max_length=256, null=True)
    expire_at = models.DateTimeField('expire time', null=True)
    scan_result = models.SmallIntegerField('扫码结果', null=True, choices=WechatQRScanResultCode.choices())
    message = models.CharField('处理结果', max_length=128, null=True)
    invitation_code = models.CharField('邀请码', max_length=16, null=True)

    class Meta:
        db_table = 'wechat_qr'

    SCAN_RESULT_MESSAGE_MAPPING = {
        0: '成功',
        1: '用户尚未注册，请注册后再试',
        2: '该微信已绑定其他账户',
    }

    def save(self, *args, **kwargs):
        if self.scan_result is not None:
            self.message = self.SCAN_RESULT_MESSAGE_MAPPING.get(self.scan_result, '未知错误')
        if not self.expire_at:
            self.expire_at = self.created_at + timezone.timedelta(seconds=self.expire_seconds)
        super(WechatQR, self).save(*args, **kwargs)
