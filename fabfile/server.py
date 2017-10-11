#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import *


def active_one(branch='', programs=None, is_sudo=True):
    do = sudo if is_sudo else run
    git_branch = branch if not branch else "origin/%s" % branch
    if not programs:
        print("没有指定部署的程序programs:%s" % programs)
        return
    with cd(env.base_dir), prefix('workon alpha'):
        do('git stash')
        do('git fetch origin')
        do('git checkout -f  %s' % git_branch)
        do('pip install -r requirements.txt -q')
        do('supervisorctl restart %s' % programs)


# 支持的 programs 写在下面
@task
def spider(branch='', is_sudo=True):
    '''
    后端代码爬虫部署
    '''
    env.base_dir = '/root/alpha'
    programs = 'spider:*'
    active_one(branch, programs, is_sudo)


@task
def api(branch='', is_sudo=True):
    '''
    后端代码API部署
    '''
    env.base_dir = '/home/exingcai/product/Alpha'
    programs = 'api:*'
    active_one(branch, programs, is_sudo)


@task
def alert(branch='', is_sudo=True):
    '''
    后端代码预警部署
    '''
    env.base_dir = '/home/exingcai/product/Alpha'
    programs = 'alert'
    active_one(branch, programs, is_sudo)


@task
def calculation(branch='', is_sudo=True):
    '''
    后端代码计算公式部署
    '''
    env.base_dir = '/home/exingcai/product/Alpha'
    programs = 'calculation'
    active_one(branch, programs, is_sudo)


@task
def futures_quant(branch='', is_sudo=True):
    '''
    后端代码十字星回测部署
    '''
    env.base_dir = '/home/exingcai/product/Alpha'
    programs = 'futures_quant'
    active_one(branch, programs, is_sudo)


@task
def preprocess(branch='', is_sudo=True):
    '''
    后端代码预处理部署
    '''
    env.base_dir = '/home/exingcai/product/Alpha'
    programs = 'preprocess'
    active_one(branch, programs, is_sudo)


@task
def schedule(branch='', is_sudo=True):
    '''
    任务调度类
    '''
    env.base_dir = '/home/exingcai/product/Alpha'
    programs = 'schedule'
    active_one(branch, programs, is_sudo)


@task
def activate(branch='', is_sudo=True):
    '''
    后端代码类
    '''
    spider(branch, is_sudo)
    api(branch, is_sudo)
    alert(branch, is_sudo)
    calculation(branch, is_sudo)
    futures_quant(branch, is_sudo)
    preprocess(branch, is_sudo)
    schedule(branch, is_sudo)
