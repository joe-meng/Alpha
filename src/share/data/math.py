# coding: utf-8
import ast

from .abc import BaseData
from .exceptions import MathCodeError


class Transfer(ast.NodeTransformer):

    def visit_Num(self, node):
        return node.n

    def visit_Name(self, node):
        return ast.Str(s=node.id)

    def visit_Attribute(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        s = '%s.%s' % (node.value.s, node.attr)
        return ast.Str(s=s)

    def visit_Call(self, node):
        from .proxy import ProxyData
        ast.NodeTransformer.generic_visit(self, node)
        data_type = node.func.s
        args = [arg.s for arg in node.args]
        args.append(data_type)
        return ProxyData(*args)

    def visit_BinOp(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node.op(node.left, node.right)

    def visit_Add(self, node):
        return lambda x, y: x + y

    def visit_Sub(self, node):
        return lambda x, y: x - y

    def visit_Mult(self, node):
        return lambda x, y: x * y

    def visit_Div(self, node):
        return lambda x, y: x / y

    def visit_Mod(self, node):
        return lambda x, y: x % y


class Math(BaseData):

    table = 'math'
    column = 'math_column'

    def __init__(self, data_code, start=None, end=None, limit=None, offset=None, desc=False):
        try:
            body = ast.parse(data_code.strip()).body
        except SyntaxError:
            raise MathCodeError('math code error: %s' % data_code)
        if len(body) == 1 and isinstance(body[0], ast.Expr):
            expr = body[0]
            visitor = Transfer()
            visitor.visit(expr)
            self.data_obj = expr.value
        else:
            raise MathCodeError('math code error: %s' % data_code)
        self.data_code = data_code
        super().__init__(self.data_code, start, end, limit, offset, desc)

    @property
    def Table(self):
        return self.data_obj.Table

    @property
    def Column(self):
        return self.data_obj.Column

    @property
    def Date(self):
        return self.data_obj.Date

    @property
    def column(self):
        return self.data_obj.column

    @property
    def date(self):
        return self.data_obj.date
