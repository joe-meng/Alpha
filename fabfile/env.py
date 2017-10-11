#!/usr/bin/env python
# -- coding: utf-8 --

from fabric.state import env

# env.use_ssh_config = True

# 要部署的服务器
env.roledefs = {
    'develop': ['exingcai@172.16.88.140:22'],
    'test': ['exingcai@172.16.88.163:22'],
    'product': ['exingcai@192.168.0.204:22'],

}
env.passwords = {
    'exingcai@172.16.88.140:22': 'exingcaitest',
    'exingcai@172.16.88.163:22': 'exingcaitest',
    'exingcai@192.168.0.204:22': 'exingcaitest',
}
