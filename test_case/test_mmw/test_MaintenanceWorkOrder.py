import unittest
import os
import json
from ddt import ddt, data
from common.handle_excel import HandleExcel
from common.handle_config import HandleConfig
from common.project_path import testData_dir
from common.handle_request import HandleRequest
from common.handle_log import logger
file_name = eval(HandleConfig().get_value('commonFrontdeviceHealth.ini', 'excel', 'file_name'))
sheet_name = eval(HandleConfig().get_value('commonFrontdeviceHealth.ini', 'excel', 'sheet_name_maintenanceWorkOrder'))
file_name = os.path.join(testData_dir, file_name)
test_data = HandleExcel(file_name, sheet_name).read()
print(test_data)


@ddt
class Test_MaintenanceManagmentWeb(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = eval(HandleConfig().get_value('common.ini', 'url', 'url'))
        cls.requeset = HandleRequest()

    def setUp(self):
        self.num = 0


    @data(*test_data)
    def test_search(self, test_data):
        curl = ''.join([self.url, test_data['url']])
        self.num = test_data['id']
        self.__dict__['_testMethodDoc'] = test_data['description']
        logger.info(f'>>>>>>>>>>>>>正在进行第【{test_data["id"]}】条测试用例<<<<<<<<<<<<<<<')
        logger.info(f'测试标题为>>>>>>>>>>>>>>>>：{test_data["description"]}')
        logger.info(f'请求方法为>>>>>>>>>>>>>>>>：{test_data["method"]}')
        logger.info(f'接口地址为>>>>>>>>>>>>>>>>：{curl}')
        logger.info(f'测试参数为>>>>>>>>>>>>>>>>：{test_data["data"]}')

        res = self.requeset.request(test_data['method'], curl, data=eval(test_data["data"]))

        try:
            self.assertEqual(eval(test_data['expect'])['code'], res.json()['code'], msg='不一致')
            self.assertEqual(eval(test_data['expect'])['codeRemark'], res.json()['codeRemark'], msg='不一致')
            logger.info(f'预期结果为>>>>>>>>>>>>>>>>：{test_data["expect"]}')
            logger.info(f'返回结果为>>>>>>>>>>>>>>>>：{res.json()}')
            logger.info(f'>>>>>>>>>>>>>第【{self.num}】条用例执行成功<<<<<<<<<<<<<<<')

        except Exception as e:
            logger.info(f'>>>>>>>>>>>>>第【{self.num}】条用例执行失败<<<<<<<<<<<<<<<')
            logger.error(f'返回结果为>>>>>>>>>>>>>>：{res}')
            raise e

    def tearDown(self):
        logger.info(f'>>>>>>>>>>>>>第【{self.num}】条用例执行完成<<<<<<<<<<<<<<<\n\n\n\n\n')


    @classmethod
    def tearDownClass(cls):
        pass
