# -- coding: utf-8 --
import os
import sys
import json
import datetime

sys.path.append("../..")

from share.utils import RedisDB

redis_handler = RedisDB

def get_redis_hash(key):
    return redis_handler.hgetall(key)

def get_redis_hash_value(key, name):
    return redis_handler.hget(key, name)

def set_redis_hash(key, name, value):
    redis_handler.hset(key, name, value)

def main():
    pass

if __name__ == '__main__':
    main()
