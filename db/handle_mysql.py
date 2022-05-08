# -*- coding: utf-8 -*-
# @Time    : 2020/1/2 12:03
# @Author  : Xu
# @File    : handle_mysql.py
# @Software: PyCharm

import pymysql
from common.handle_config import HandleConfig


class HandleMySql(object):
    """
    封装MySQL查询
    """

    def __init__(self,config):
        """
        初始化MySQL对象
        """
        # 返回一个数据库连接
        self.config = HandleConfig()
        self.db_name = eval(self.config.get_value('common.ini','db',config))
        self.db = pymysql.connect(**self.db_name, use_unicode="utf-8")
        self.cursor = self.db.cursor()

    def get_description(self):
        '''
        获取表的字段
        :return: 表的字段
        '''

        key = [i[0] for i in self.cursor.description]
        return key


    def query(self, sql):
        """
        返回查询结果
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result_list = []
        if result:
            key = self.get_description()
            for value in result:
                result_dict = {}
                for i in range(len(key)):
                    result_dict[key[i]] = value[i]
                result_list.append(result_dict)
        else:
            print("没有查询到结果")
        self.close()
        return result_list

    def query_one(self, sql):
        """
        返回查询到的第一条数据
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        result_one = self.cursor.fetchone()
        result_one_list = []
        if result_one:
            result_one_dict = {}
            key = self.get_description()
            for i in range(len(key)):
                result_one_dict[key[i]] = result_one[i]
            result_one_list.append(result_one_dict)
        else:
            print("没有查询到结果")
        self.close()
        return result_one_list

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()


if __name__ == '__main__':
    db = HandleMySql('config')
    # result = db.query('select * from sys_department')
    # print(result)
    print(db.get_description())
