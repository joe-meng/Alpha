# -- coding: utf-8 --
import ast

import logging

logger = logging.getLogger(__name__)

EXPR_BLACK_LIST = set(['exec', 'compile', 'eval', 'open'])


class FormulaSecurityError(Exception):
    pass


def expr_black_list_check(module_name):
    if module_name in EXPR_BLACK_LIST:
        raise FormulaSecurityError('禁止使用非法方法：%s' % module_name)


def security_check(code_str):
    ast_nodes = list(ast.walk(ast.parse(code_str, mode='exec')))

    # 过滤 import
    import_nodes = list(filter(lambda i: isinstance(i, (ast.Import, ast.ImportFrom)), ast_nodes))
    if import_nodes:
        raise FormulaSecurityError('禁止导入任何包')

    # 过滤一些内置方法
    expr_nodes = list(filter(lambda i: isinstance(i, ast.Expr), ast_nodes))
    for expr_node in expr_nodes:
        try:
            expr_black_list_check(expr_node.value.func.id)
        except AttributeError as e:
            logger.warning('expr_node: %s %s' % (ast.dump(expr_node), e.args[0]))
            continue
