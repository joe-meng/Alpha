# coding: utf-8
import os
import importlib
import uuid
import sys


class ConfigFinder(object):

    def __init__(self, nodes_env, configs):
        self.nodes_env = nodes_env
        self.configs = configs

    @staticmethod
    def getnode():
        return str(uuid.getnode())

    @property
    def env(self):
        return self.nodes_env.get(self.getnode()) or 'default'

    def find_module(self):
        module_path = self.configs.get(self.env) or self.configs.get('default')
        try:
            module = importlib.import_module(module_path)
        except ImportError:
            raise
        return module

share_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(share_path)
if src_path not in sys.path:
    sys.path.append(src_path)
nodes = {'167132875207439': 'test',  # jeff mac
         '345051417773': 'develop',  # 开发环境
         '345051415229': 'test',  # 测试环境
         '345051394857': 'product'}  # 生产环境
config_path = {'default': 'share.settings.defaults',
               'develop': 'share.settings.develop',
               'test': 'share.settings.test',
               'product': 'share.settings.prod'}
finder = ConfigFinder(nodes, config_path)
config_module = finder.find_module()
mysql = {'host': config_module.DATABASES['default']['HOST'],
         'port': config_module.DATABASES['default']['PORT'],
         'user': config_module.DATABASES['default']['USER'],
         'password': config_module.DATABASES['default']['PASSWORD'],
         'db': config_module.DATABASES['default']['NAME'],
         'charset': 'utf8',
         'timeout': 7200}

mq = {"host": config_module.MQ_HOST}
