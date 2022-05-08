import cx_Oracle
import os
from common.handle_config import HandleConfig
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'



class HandleOracle:
    def __init__(self):
        '''
        初始化，连接数据库
        '''
        self.oracle_connect = eval(HandleConfig().get_value('common.ini', 'db', 'oracle'))
        self.db = cx_Oracle.connect(self.oracle_connect)
        self.cur = self.db.cursor()

    def __get_description(self):
        '''
        取出表的字段
        :return: 表字段的列条
        '''
        return [i[0] for i in self.cur.description]

    def query(self,sql):
        '''
        返回全部的数据
        :param sql: sql语句
        :return:返回数据库中的数据（result_list）
        '''
        self.cur.execute(sql)
        result = self.cur.fetchall()
        key = self.__get_description()
        result_list = []
        if result:
            for value in result:
                result_dict  = {}
                for i in range(len(key)):
                    result_dict[key[i]] = value[i]
                result_list.append(result_dict)
        else:
            print("没有查询到结果")
        self.__close()
        return result_list

    def query_one(self,sql):
        '''
        返回第一条数据
        :param sql: sql语句
        :return:返回数据库中的数据（result_one_list）
        '''
        self.cur.execute(sql)
        result_one = self.cur.fetchone()
        key = self.__get_description()
        result_one_list = []
        if result_one:
            result_one_dict = {}
            for i in range(len(key)):
                result_one_dict[key[i]] = result_one[i]
            result_one_list.append(result_one_dict)
        else:
            print("没有查询到结果")
        self.__close()
        return result_one_list

    def query_many(self,sql,many):
        '''
        感觉参数返回几条数据
        :param sql: sql语句
        :param many: 返回数据的条数
        :return:返回数据库中的数据（result_many_list）
        '''
        self.cur.execute(sql)
        result_many = self.cur.fetchmany(many)
        key = self.__get_description()
        result_many_list = []
        if result_many:
            result_many_dict = {}
            for value in result_many:
                for i in range(len(key)):
                    result_many_dict[key[i]] = value[i]
            result_many_list.append(result_many_dict)
        else:
            print("没有查询到结果")
        self.__close()
        return result_many_list

    def insert(self, sql, param):
        try:
            self.cur.executemany(sql, param)
            self.db.commit()
            print("插入成功")
        except Exception as e:
            print(e)
        finally:
            self.__close()

    def update(self, sql):
        """
        对数据进行更新操作
        :param sql: sql语句
        """
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.__close()

    def delete(self,sql):
        """
        对数据进行删除操作
        :param sql: sql语句
        """
        try:
            self.cur.execute(sql)
            result = self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.__close()

    def __close(self):
        '''
        关闭游标
        关闭数据库连接
        :return:None
        '''
        if self.cur:
            self.cur.close()
        if self.db:
            self.db.close()



if __name__ == '__main__':
    db = HandleOracle()
    sql = "SELECT * FROM COMMON_FRONTDEVICE_GROUP where DEVICEGROUPNAME = '自动化测试-001'"
    data = db.query_one(sql)
    print(data)



