# coding: utf-8
from sqlbuilder.smartsql import Result, Q
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData


class _Math(BaseData):
    column = '_math_column'
    date = 'math_date'

    def __init__(self, left, right):
        self._table = None
        self.left = left
        self.right = right

    @property
    def Table(self):
        if not self._table:
            self._table = self._get_table()
        return self._table

    def _get_table(self):
        q = Q(self.left.Table, result=Result(mysql_compile))
        if isinstance(self.right, BaseData):
            q = q.tables(q.tables() + self.right.Table).on(self.left.Date == self.right.Date)
            right_column = self.right.Column
        else:
            right_column = self.right
        column = self._get_column(right_column)
        date = self.left.Date.as_(self.date_alias)
        q = q.fields(column, date)
        return q.as_table(str(id(self)))

    def _get_column(self, right_column):
        raise NotImplemented


class Add(_Math):
    column = 'add_column'
    date = 'add_date'

    def _get_column(self, right_column):
        return (self.left.Column + right_column).as_(self.column)


class Sub(_Math):
    column = 'sub_column'
    date = 'sub_date'

    def _get_column(self, right_column):
        return (self.left.Column - right_column).as_(self.column)


class Rsub(_Math):
    column = 'rsub_column'
    date = 'rsub_date'

    def _get_column(self, right_column):
        return (right_column - self.left.Column).as_(self.column)


class Mult(_Math):
    column = 'mult_column'
    date = 'mult_date'

    def _get_column(self, right_column):
        return (self.left.Column * right_column).as_(self.column)


class Div(_Math):
    column = 'div_column'
    date = 'div_date'

    def _get_column(self, right_column):
        return (self.left.Column / right_column).as_(self.column)


class Rdiv(_Math):
    column = 'rdiv_column'
    date = 'rdiv_date'

    def _get_column(self, right_column):
        return (right_column / self.left.Column).as_(self.column)


class Mod(_Math):
    column = 'mod_column'
    date = 'mod_date'

    def _get_column(self, right_column):
        return (self.left.Column % right_column).as_(self.column)


class Rmod(_Math):
    column = 'rmod_column'
    date = 'rmod_date'

    def _get_column(self, right_column):
        return (right_column % self.left.Column).as_(self.column)
