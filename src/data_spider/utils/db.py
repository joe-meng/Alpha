# -*- coding: utf-8 -*-
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import MySQLdb.cursors

class MysqlHnadler(object):
    """docstring for MysqlHnadler."""

    def __init__(self, table_name, db_name='alpha', host="140"):
        self.db_name = db_name
        self.table = table_name
        if host=="250":
            self.db = self.get_250_mysql_db()
        elif host == "140":
            self.db = self.get_140_mysql_db()
        elif host == "43":
            self.db = self.get_43_mysql_db()
        elif host == "163":
            self.db = self.get_163_mysql_db()
        elif host == "204":
            self.db = self.get_204_mysql_db()
        else:
            self.db = self.get_140_mysql_db()
        self.cursor = self.db.cursor()

    def get_43_mysql_db(self):
        db = MySQLdb.connect(
            host='211.152.46.43',
            port = 3306,
            user='deploy',
            passwd='9i[1sF&#2>nBo!*z',
            db = 'alpha',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset='utf8'
        )
        return db

    def get_140_mysql_db(self):
        db = MySQLdb.connect(
            host='172.16.88.140',
            port = 20306,
            user='exingcai',
            passwd='uscj!@#',
            db = 'alpha',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset='utf8'
        )
        return db

    def get_163_mysql_db(self):
        db = MySQLdb.connect(
            host='172.16.88.163',
            port = 20306,
            user='exingcai',
            passwd='uscj!@#',
            db = 'alpha',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset='utf8'
        )
        return db

    def get_204_mysql_db(self):
        db = MySQLdb.connect(
            host='192.168.0.204',
            port = 20306,
            user='exingcai',
            passwd='uscj!@#',
            db = 'alpha',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset='utf8'
        )
        return db

    def get_250_mysql_db(self):
        db = MySQLdb.connect(
            host='139.196.48.250',
            port = 3306,
            user='root',
            passwd='uscjQAZ',
            db = 'ie',
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
        # print(insert_str)
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
                    where_str += "and %s in (%s,)"%(key, where_dict[key][0])
                else:
                    where_str += "and %s in %s"%(key, tuple(where_dict[key]))
            else:
                where_str += "and %s='%s'"%(key, where_dict[key])
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
        # print(sql_str)
        self.cursor.execute(sql_str)
        if find_all:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def query_by_sql(self, sql_str, find_all=0):
        # 根据sql语句查询
        print(sql_str)
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
        print(update_str)
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



def main():
    pass
    # handler = MysqlHnadler("foreign_exchange")
    # handler.insert_table_info({"title": "好的", "data":"12312.123","base":"rmd", "date_record":"2017-09-12"})
    # handler.commit()
    # handler.close()

if __name__ == '__main__':
    main()
