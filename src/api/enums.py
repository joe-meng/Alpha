# -- coding: utf-8 --
import enum


class EnumToChoicesMixin(object):

    @classmethod
    def values(cls):
        return [i.value for i in cls]

    @classmethod
    def choices(cls):
        return [(i.value, i.name) for i in cls]


class FeeTypes(EnumToChoicesMixin, enum.Enum):
    """
    费用类型
    """
    domestic_processing_fee = 1
    import_processing_fee = 2
    miscellaneous_fee = 3


class VarietiesAmountTypes(EnumToChoicesMixin, enum.Enum):
    """
    品类数量类型
    """
    imports = 1
    exports = 2
    production = 3


class WechatSexTypes(EnumToChoicesMixin, enum.Enum):
    """
    微信性别
    """
    null = 0
    male = 1
    female = 2


class WechatQRCodeActionNameTypes(EnumToChoicesMixin, enum.Enum):
    """
    二维码类型
    """
    QR_SCENE = 'QR_SCENE'
    QR_STR_SCENE = 'QR_STR_SCENE'
    QR_LIMIT_SCENE = 'QR_LIMIT_SCENE'
    QR_LIMIT_STR_SCENE = 'QR_LIMIT_STR_SCENE'


class WechatQRScanResultCode(EnumToChoicesMixin, enum.Enum):
    """
    二维码扫描结果
    """
    WAIT = None
    SUCCESS = 0
    NOT_REGISTERED = 1
    ALREADY_BOUND = 2       # 微信号已绑定其他手机号
    NOT_REAL_NAMED = 3

class TableTypes(EnumToChoicesMixin, enum.Enum):
    LOCATION = 0
    HISTORY = 1
    SQL = 2
