# -*- coding: utf-8 -*-
# @Time    : 2019/12/27 14:27
# @Author  : Xu
# @File    : runner.py
# @Software: PyCharm
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import unittest
from BeautifulReport import BeautifulReport
from common.handle_log import logger
from common.project_path import testCase_dir,report_dir
import time

# 创建测试套件


suite = unittest.defaultTestLoader.discover(testCase_dir, pattern='test*.py')
# filename = time.strftime("%Y%m%d%H%M%S")
filename = time.strftime("%Y-%m-%d")
BeautifulReport(suite).report(description="接口自动化", filename=filename, report_dir=report_dir)
logger.info(f"测试已全部完成, 可前往[{report_dir}]查询测试报告")
