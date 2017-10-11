#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import *


@task
def activate(branch='', programs=None, is_sudo=True):
    '''
    前端代码类
    '''
    print("前端部署等待实现")