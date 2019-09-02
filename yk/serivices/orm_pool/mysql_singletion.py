import pymysql
from orm_pool.db_pool import POOL


class Mysql(object):
    def __init__(self):
        self.conn = POOL.connection()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def select(self, sql, *args):
        self.cursor.execute(sql, args)
        res = self.cursor.fetchall()
        return res

    def execute(self, sql, args):
        try:
            self.cursor.execute(sql, args)
        except BaseException as e:
            print(e)
