# -- coding: utf-8 --
import os
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except :
    pass

import redis
import MySQLdb
import MySQLdb.cursors


from share.settings.defaults import get_env

cur_env = get_env()

# cur_env = {
#     'ENGINE': 'django.db.backends.mysql',
#     'USER': 'exingcai',
#     'PORT': 20306,
#     'HOST': '172.16.88.140',
#     'NAME': 'alpha',
#     'PASSWORD': 'uscj!@#',
#     'MQ_HOST': '172.16.88.140',
# }

class MysqlHnadler(object):
    """docstring for MysqlHnadler."""

    def __init__(self, table_name, db_name=cur_env['NAME']):
        # 初始化handler内容
        self.db_name = db_name
        self.table = table_name
        self.db = self.get_mysql_db()
        self.cursor = self.db.cursor()

    def get_mysql_db(self):
        """
        * desc    获取表的handler
        * input   None
        * output  db的handler
        """
        db = MySQLdb.connect(
            host = cur_env['HOST'],
            port = cur_env['PORT'],
            user = cur_env['USER'],
            passwd = cur_env['PASSWORD'],
            db = self.db_name,
            cursorclass = MySQLdb.cursors.DictCursor,
            charset='utf8'
        )
        return db

    def insert_table_info(self, insert_dict):
        """
        * desc    给表插入一条数据
        * input   要插入的字段内容
        * output  无
        """
        ROWstr = ''  #行字段
        COLstr = ''  # 列字段
        for key in insert_dict.keys():
            COLstr = (COLstr+'`%s`'+',')%key
            ROWstr = (ROWstr+'"%s"'+',')%insert_dict[key]
        insert_str = """  insert into %s (%s) VALUES (%s)"""%(self.table, COLstr[:-1], ROWstr[:-1])
        self.cursor.execute(insert_str)
        return self.cursor.lastrowid

    def query(self, where_dict, find_all=0, order_by=None, limit=None):
        """
        * desc 查询
        """
        where_str = ""
        for key in where_dict.keys():
            if isinstance(where_dict[key], list):
                if len(where_dict[key])==1:
                    where_str += " and %s in (%s,)"%(key, where_dict[key][0])
                else:
                    where_str += " and %s in %s"%(key, tuple(where_dict[key]))
            else:
                where_str += "and %s='%s' "%(key, where_dict[key])
        if where_str:
            where_str = where_str[3:]
            sql_str = """   select * from %s where %s """%(self.table, where_str)
        else:
            sql_str = """   select * from %s """%self.table
        if order_by:
            sql_str = sql_str + " order by %s desc "%order_by
        if not find_all:
            sql_str = sql_str + " limit 1"
        if limit:
            sql_str = sql_str + " limit %s"%limit
        self.cursor.execute(sql_str)
        if find_all:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def query_by_sql(self, sql_str, find_all=0):
        # 根据sql语句查询
        self.cursor.execute(sql_str)
        if find_all:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def check_exist(self, where_dict):
        # 检测是否存在该条数据
        where_str = ""
        for key in where_dict.keys():
            where_str += "and %s='%s'"%(key, where_dict[key])
        if not where_str:
            return 1
        else:
            where_str = where_str[3:]
        sql_str = """   select count(*) as count from %s where %s """%(self.table, where_str)
        self.cursor.execute(sql_str)
        info = self.cursor.fetchone()
        return info["count"]

    def update_table_info(self, update_dict, where_dict):
        """
        * desc    更新表内容
        * input   要更新的字段内容
        * output  无
        """
        update_var = ""
        where_str = ""
        for key, value in update_dict.items():
            update_var += "`{0}`='{1}',".format(key, value)
        for key, value in where_dict.items():
            where_str += "and `{0}`='{1}' ".format(key, value)
        update_str = """  UPDATE {0} SET {1} WHERE {2}; """.format(self.table, update_var[:-1], where_str[3:])
        self.cursor.execute(update_str)

    def insert_or_update(self, insert_dict, where_dict):
        # 插入或者是更新数据
        if self.check_exist(where_dict):
            self.update_table_info(insert_dict, where_dict)
        else:
            return self.insert_table_info(insert_dict)

    def change_table(self, table_name):
        self.table = table_name

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()




class RedisDB(object):
    """docstring for RedisDB"""
    def __init__(self):
        self.r = redis.Redis(connection_pool=redis.ConnectionPool(host=cur_env['REDIS_HOST'],
                        port = cur_env['REDIS_PORT'],
                        password = cur_env['REDIS_PWD'],
                        db = cur_env['REDIS_DB']
                    ))

    # 获取指定key 的value
    def get(self, key):
        if isinstance(key, list):
            return self.r.mget(key)
        else:
            return self.r.get(key)

    def keys(self):
        return self.r.keys()

    # 设置 key 对应的值为 string 类型的 value
    def set(self, key, value):
        return self.r.set(key, value)

    #设置 key 对应的值为 string 类型的 value。如果 key 已经存在,返回 0,nx 是 not exist 的意思
    def setnx(self, key, value):
        return self.r.setnx(key, value)

    #设置 key 对应的值为 string 类型的 value,并指定此键值对应的有效期
    def setex(self, key, time, value):
        return self.r.setex(key, time, value)

    #setrange name 8 gmail.com
    #其中的 8 是指从下标为 8(包含 8)的字符开始替换
    def setrange(self, key, num, value):
        return self.r.setrange(key, num, value)

    #获取指定 key 的 value 值的子字符串
    def getrange(self, key, start ,end):
        return self.r.getrange(key, start, end)

    #删除
    def remove(self, key):
        return self.r.delete(key)
    #自增
    def incr(self, key, default = 1):
        if (1 == default):
            return self.r.incr(key)
        else:
            return self.r.incr(key, default)
    #自减
    def decr(self, key, default = 1):
        if (1 == default):
            return self.r.decr(key)
        else:
            return self.r.decr(key, default)

    #2. hashes 类型及操作
    def hget(self, key, name):
        return self.r.hget(key, name)

    # 设置hash的值
    def hset(self, key, name, value):
        return self.r.hset(key, name, value)

    #获取哈希表中的所有数据
    def hgetall(self, key):
        return self.r.hgetall(key)

    #删除hashes
    def hdel(self, name, key = None):
        # 删除哈希表 key 中的一个或多个指定域，不存在的域将被忽略。
        if(key):
            return self.r.hdel(name, key)
        return self.r.hdel(name)

    def hexists(self, name, key):
        # return a boolean indicating if the key within hash name
        # 如果哈希表含有给定域，返回 1 。
        # 如果哈希表不含有给定域，或 key 不存在，返回 0 。
        self.r.hexists()
        return self.r.hexists(name, key)

    def hlen(self, name):
        # return the length of name
        # 哈希表中域的数量
        return self.r.hlen(name)

    def hmget(self, name, *keys):
        # 返回哈希表 key 中，一个或多个给定域的值。
        # 如果给定的域不存在于哈希表，那么返回一个 nil 值。
        return self.r.hmget(name, *keys)

    def hsetnx(self, name, key, value):
        # 将哈希表 key 中的域 field 的值设置为 value ，当且仅当域 field 不存在。
        return self.r.hsetnx(name, key, value)

    def hvals(self, name):
        # return the list value of hash name has
        # 返回哈希表 key 中所有域的值。
        return self.r.hvals(name)

    # def hmset(self):
    #     return self.r.hmset(name, mapping)

    #清空当前db
    def clear(self):
        return self.r.flushdb()

    #3、lists 类型及操作
    #适合做邮件队列

    def lindex(self, key, value):
        return self.r.lindex(key, value)

    # 获取list的长度
    def llen(self, key):
        return self.r,llen(key)

    #在 key 对应 list 的头部添加字符串元素
    def lpush(self, key ,value):
        return self.r.lpush(key, value)

    def rpush(self, key, value):
        return self.r.rpush(key, value)

    #从 list 的尾部删除元素,并返回删除元素

    def lpop(self, key):
        return self.r.lpop(key)

    def rpop(self, key):
        return self.r.rpop(key)

    def lrem(self, name, value):
        # 删除name中list等于value的值
        return self.r.lrem(name, value, num=0)

    def ltrim(self, name, start, end):
        return self.r.ltrim(name, start, end)

    def lrange(self, namelist, start, end):
        return self.r.lrange(namelist, start, end)
