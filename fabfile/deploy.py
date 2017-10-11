#!/usr/bin/env python
# -- coding: utf-8 --
from fabric.api import *

from . import html, server


@task(default=True)
def deploy(branch='', is_sudo=True):
    '''
    前端后端代码部署
    '''
    server.activate(branch, is_sudo)
    html.activate(branch, is_sudo)


@task
def deploy_server(branch='', is_sudo=True):
    '''
    后端代码部署
    '''
    from . import server
    server.activate(branch, is_sudo)


@task
def deploy_html(branch='', is_sudo=True):
    '''
    前端代码部署
    '''
    from . import html
    html.activate(branch, is_sudo)
