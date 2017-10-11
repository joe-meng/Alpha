# coding: utf-8


class DataException(Exception):
    pass


class SymbolNotExists(DataException):
    pass


class ShipNotExists(DataException):
    pass


class SerialNotExists(DataException):
    pass


class DefaultCodeError(DataException):
    pass


class SymbolCodeError(DataException):
    pass


class KlineCodeError(DataException):
    pass


class SerialCodeError(DataException):
    pass


class ContractCodeError(DataException):
    pass


class MathCodeError(DataException):
    pass


class FutureCodeError(DataException):
    pass
