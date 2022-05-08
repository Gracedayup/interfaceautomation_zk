#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Time     : 2020/4/15 13:31
    Author   : yanw
    File       : test_commonFrontdevice.py
    Software: PyCharm
       基础数据-设备管理-设备信息
    """


from common.handle_excel import HandleExcel
from common.handle_config import HandleConfig
from common.handle_request import HandleRequest
from common.project_path import testData_dir
from common.handle_log import logger
from db.handle_oracle import HandleOracle
from ddt import ddt,data
import unittest
import os
file_name = eval(HandleConfig().get_value('basicdata.ini', 'excel', 'file_name'))
sheet_name = eval(HandleConfig().get_value('basicdata.ini', 'excel', 'commonFrontdevice_sheet_name'))
file_name = os.path.join(testData_dir, file_name)
commonFrontdevice_data = HandleExcel(file_name, sheet_name).read()

@ddt
class Basic_Data(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            cls.url = eval(HandleConfig().get_value('common.ini', 'url', 'url'))
            cls.requeset = HandleRequest()

        def setUp(self):
            logger.info(f'>>>>>>>>>>>>>开始执行测试用例<<<<<<<<<<<<<<<')
            self.db = HandleOracle()

        @data(*commonFrontdevice_data)
        def test_commonFrontdevice(self,test_data):
            # 拼接接口url
            curl = ''.join([self.url, test_data['url']])
            # 测试报告的描述
            self.__dict__['_testMethodDoc'] = test_data['description']
            logger.info(f'>>>>>>>>>>>>>正在进行第【{test_data["id"]}】条测试用例<<<<<<<<<<<<<<<')
            logger.info(f'测试标题为>>>>>>>>>>>>>>>>：{test_data["description"]}')
            logger.info(f'请求方法为>>>>>>>>>>>>>>>>：{test_data["method"]}')
            logger.info(f'接口地址为>>>>>>>>>>>>>>>>：{curl}')
            if test_data['data']:
                if  str(test_data["is_replace"]).lower() == 'true':
                    sql  = eval(test_data['data'])['SQL']
                    data = self.db.query_one(sql)
                    param = eval(test_data['data'])['param']
                    if (type(param).__name__ == 'list'):
                        for data_dic in param:
                            for key in data_dic:
                                if key == 'deviceid':
                                    data_dic[key] = data[0]['DEVICEID']
                                elif key == 'deviceId':
                                    data_dic[key] = data[0]['DEVICEID']
                    elif (type(param).__name__ == 'dict'):
                        for key in param:
                            if key == 'deviceid':
                                param[key] = data[0]['DEVICEID']
                            elif key == 'deviceId':
                                param[key] = data[0]['DEVICEID']
                            elif key == 'deviceIdList':
                                param[key] = [data[0]['DEVICEID'] if i == 'string' else i for i in param[key]]
                    if str(test_data['method']).lower() == 'delete' or str(test_data['method']).lower()  == 'post':
                        if not str(test_data["is_json"]).lower() == 'true':
                            param = param['deviceid'].split()
                        # else:
                        #     param = param['deviceid'].split()
                    logger.info(f'测试参数为>>>>>>>>>>>>>>>>：{param}')
                    res = self.requeset.request(test_data['method'], curl, data=param)
                else:
                    logger.info(f'测试参数为>>>>>>>>>>>>>>>>：{test_data["data"]}')
                    res = self.requeset.request(test_data['method'], curl, data=eval(test_data['data']))
            else:
                logger.info(f'测试参数为>>>>>>>>>>>>>>>>：{test_data["data"]}')
                res = self.requeset.request(test_data['method'], curl)
            try:
                self.assertEqual(eval(test_data['expect'])['code'], res.json()['code'], msg='不一致')
                self.assertEqual(eval(test_data['expect'])['codeRemark'], res.json()['codeRemark'], msg='不一致')
            except Exception as e:
                logger.info(f'>>>>>>>>>>>>>第【{test_data["id"]}】条用例执行失败<<<<<<<<<<<<<<<')
                logger.error(f'返回结果为>>>>>>>>>>>>>>：{res}')
                raise e

        def tearDown(self):
            logger.info(f'>>>>>>>>>>>>>执行测试用例结束<<<<<<<<<<<<<<<')

        @classmethod
        def tearDownClass(cls):
            pass

