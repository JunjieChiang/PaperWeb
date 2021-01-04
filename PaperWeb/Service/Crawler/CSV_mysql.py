import csv
import time
import pymysql
import logging

path = r"C:\Users\14124\Desktop\MyProject\5.PaperWeb\Service\Crawler\paper.csv"

class MySQLDB(object):
    def __init__(self, host="localhost", port=3306, user="root", passwd="root", db="test"):
        # cursorclass=pymysql.cursors.DictCursor 默认返回tuple, 需要将数据库返回内容转换为dict
        self.connect = pymysql.connect(host=host,
                                       port=port,
                                       user=user,
                                       passwd=passwd,
                                       db=db,
                                       charset="utf8",
                                       cursorclass=pymysql.cursors.DictCursor)      # 转换成字典

        self.log = logging.getLogger(__name__)


    def execute(self, sql, kwargs=None):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, kwargs)
            self.connect.commit()           # 将插入、删除 commit / 查询
            return cursor

        except Exception as e:
            self.log.error("mysql execute error:{e}", exc_info=True)
            raise e

    def query(self, sql, kwargs=None):
        cursor = None
        try:
            cursor = self.execute(sql, kwargs)
            if cursor:
                return cursor.fetchall()  # 查询的所有内容，dict
            else:
                raise Exception(f"sql error:{sql}")

        except Exception as e:
            self.log.error(e)
            raise e
        finally:
            if cursor:
                cursor.close()

    def insert(self, sql, kwargs=None):
        cursor = None
        try:
            cursor = self.execute(sql, kwargs)
            if cursor:
                row_id = cursor.lastrowid       # 最后一行id
                return row_id
            else:
                raise Exception(f"sql error:{sql}")

        except Exception as e:
            self.log.error(e)
            raise e
        finally:
            if cursor:
                cursor.close()

    def escape_string(self, _):         # 转码
        return pymysql.escape_string(_)     # 编译

db = MySQLDB(user="root", passwd="jiangjunjie189", db="paper")                   # 实例化

def get_csv_info(path):
    csvfile = open(path, "r")
    reader = csv.reader(csvfile)
    for item in reader:
        yield item

def get_insert_sql():
    items = []
    _time = int(time.time())
    for item in get_csv_info(path):
        item = [db.escape_string(_) for _ in item]
        # insert sql values
        items.append(f"('{item[0]}', '{item[1]}', '{item[2]}', '{_time}', '{_time}')")

    values = ", ".join(items)
    sql = f'''
    INSERT INTO
     papers(`title`, `url`, `authors`, `create_time`, `update_time`)
    VALUES
     {values}
    '''

    row_id = db.insert(sql)
    print(f"{row_id}条数据插入完成")

if __name__ == "__main__":
    get_insert_sql()