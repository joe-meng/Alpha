# -*- coding:utf-8 -*-

import pymongo
# import MySQLdb
# import MySQLdb.cursors
# from bson.objectid import ObjectId
from pymongo import MongoClient


class MongoHandler(object):
    """docstring for MongoHandler"""
    def __init__(self, arg=None):
        # self.db.authenticate('user', 'password', mechanism='SCRAM-SHA-1')
        self.db = MongoClient(host='172.16.88.140', port=27017)['data']
        # self.db = MongoClient(host='127.0.0.1', port=27017)['data']

    def insert_one(self, collection_name, info):
        """
        * desc   插入一条数据
        * input  collection name   要插入的内容
        * output 插入后生成的id
        """
        info.update({
            "machine_class":"",
            "machine_summary":"",
            "machine_tags":"",
            "look_state":"0",
            "pub_state":"0",
            "push_state":"0",
        })
        return self.db[collection_name].insert_one(info).inserted_id

    def insert_many(self, collection_name, info_list):
        """
        * desc    插入多条数据
        * input   collection name 要插入的列表信息
        * output  插入后的id列表
        """
        return self.db[collection_name].insert_many(info_list).inserted_ids

    def find_one(self, collection_name, where={}):
        """
        * desc   获取一条数据
        * input  collection name 查询的条件
        * output 查询出来的一条内容
        """
        result = self.db[collection_name].find_one(where)
        if not result.count():
            result = {}
        return result

    def find(self, collection_name, where={}):
        """
        * desc    查询所有的内容
        * input   collection name 查询的条件
        * output  能够找到的所有的内容
        """
        result = self.db[collection_name].find(where)
        if not result.count():
            result = []
        return result

    def count(self, collection_name, where={}):
        """
        * desc   获取查询的数量
        * input  collection name 查询的条件
        * output 数量
        """
        return self.db[collection_name].count()

    def remove(self, collection_name, where={}):
        """
        * desc   删除历史记录信息
        * input  collection name 删除条件
        * output 无
        """
        self.db[collection_name].remove(where)

    def remove_one(self, collection_name, where={}):
        """
        * desc   删除一条数据
        * input  collection name 删除条件
        * output 无
        """
        self.db[collection_name].find(where).remove_one()

    def create_index(self, collection_name, col_name, sequence=1, unique=False):
        """
        * desc    创建索引
        * input   collection name 要建索引列的名字  正序或者倒叙 是否唯一
        * output  none
        """
        if sequence:
            self.db[collection_name].create_index([(col_name, pymongo.ASCENDING)], unique=unique)
        else:
            self.db[collection_name].create_index([(col_name, pymongo.DESCENDING)], unique=unique)

    def check_exist(self, collection_name, where={}):
        """
        * desc    查看是否存在索要查找的内容
        * input   collection name 要建索引列的名字  正序或者倒叙 是否唯一   where 条件对象
        * output  1 存在  0 不存在
        """
        return 1 if self.db[collection_name].find(where).count() else 0


#
# class MysqlHnadler(object):
#     """docstring for MysqlHnadler."""
#
#     def get_mysql_db(self):
#         db = MySQLdb.connect(
#             host='139.196.48.250',
#             port = 3306,
#             user='root',
#             passwd='uscjQAZ',
#             db ='ie',
#             cursorclass = MySQLdb.cursors.DictCursor,
#             charset='utf8'
#         )
#
#         return db
#
#     def insert_table_info(self, insert_dict):
#         """
#         * desc    给表插入一条数据
#         * input   要插入的字段内容
#         * output  无
#         """
#         ROWstr = ''  #行字段
#         COLstr = ''  # 列字段
#         for key in insert_dict.keys():
#             COLstr = (COLstr+'`%s`'+',')%key
#             ROWstr = (ROWstr+'"%s"'+',')%insert_dict[key]
#         insert_str = """  insert into %s (%s) VALUES (%s)"""%(self.table, COLstr[:-1], ROWstr[:-1])
#         self.cursor.execute(insert_str)
#
#     def __init__(self, table_name):
#         self.table = table_name
#         self.db = self.get_mysql_db()
#         self.cursor = self.db.cursor()
#
#     def commit(self):
#         self.db.commit()
#
#     def close(self):
#         self.db.close()
