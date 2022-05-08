# -*- coding: utf-8 -*-
# @Time    : 2019/12/25 12:51
# @Author  : Xu
# @File    : handle_log.py
# @Software: PyCharm

import logging
from common import project_path
import datetime
import os

class HandleLog(object):
    """
    封装日志器
    """

    def __init__(self):
        # 先将配置器创建

        # 1.定义日志收集器
        now_time = datetime.datetime.now()
        date = datetime.datetime.strftime(now_time, '%Y-%m-%d')
        txt_name = ''.join([date, '.log'])
        log_dir = project_path.log_dir
        file_name = os.path.join(log_dir,txt_name)
        self.logger = logging.getLogger("case")
        # 2.指定搜集日志的等级
        self.logger.setLevel(logging.DEBUG)
        # 3.定义日志输出的渠道,指定要将日志输入的位置
        # 指定将日志输出到指定文件中
        file_handle = logging.FileHandler(file_name, mode='a', encoding="utf-8")
        # 指定将日志输出到控制台
        console_handle = logging.StreamHandler()

        # 4.指定日志输出的等级
        file_handle.setLevel(logging.DEBUG)
        console_handle.setLevel(logging.INFO)

        # 5.定义日志显示的格式
        console_formatter = logging.Formatter(
            "%(asctime)s-[%(levelname)s]-[msg]:%(message)s [Lineno]:%(lineno)d module-%(module)s")
        file_formatter = logging.Formatter(
            "%(asctime)s-[%(levelname)s]-[msg]:%(message)s-[Lineno]:%(lineno)d module-%(module)s")

        # 设置日志输入格式
        file_handle.setFormatter(file_formatter)
        console_handle.setFormatter(console_formatter)

        # 6.将日志收集器与输出管道对接
        self.logger.addHandler(file_handle)
        self.logger.addHandler(console_handle)


logger = HandleLog().logger
if __name__ == '__main__':
    logs = HandleLog()
    logger.debug("这是debug等级")
    logger.info("这是info等级")
