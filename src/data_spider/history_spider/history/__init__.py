# encoding: utf-8

"""
初始化项目依赖
:return:
"""
import os

import sys

import django

root_path = os.path.abspath(__file__ if '__file__' in locals() else os.path.curdir)
while os.path.basename(root_path).lower() != 'src':
    root_path = os.path.dirname(root_path)

sys.path.append(os.path.join(root_path, 'api'))
sys.path.append(root_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alpha.settings.defaults")
django.setup()

