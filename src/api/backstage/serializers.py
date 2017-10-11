#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@date: 2016-12-19
@author: Devin
"""

from user.models import User
from rest_framework import serializers
from rest_framework.fields import CharField


class MSUserSerializer(serializers.ModelSerializer):
    # register_step_display = CharField(
    #     source='get_register_step_display', read_only=True)
    # user_active_display = CharField(
    #     source='get_user_active_display', read_only=True)
    # user_role_type_display = CharField(
    #     source='get_user_role_type_display', read_only=True)
    # email_is_active_display = CharField(
    #     source='get_email_is_active_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username')
