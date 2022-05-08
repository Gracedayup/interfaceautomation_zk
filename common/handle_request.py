# -*- coding: utf-8 -*-
# @Time    : 2019/12/23 18:47
# @Author  : Xu
# @File    : handle_request.py
# @Software: PyCharm
import requests
from common.handle_log import logger
from common.handle_config import HandleConfig
import time
import hashlib
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning




requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


url = eval(HandleConfig().get_value('common.ini', 'url', 'url'))
interface = eval(HandleConfig().get_value('common.ini', 'url', 'login'))
# 登录URL

# login_url = os.path.join(url, interface)
login_url = '/'.join([url, interface])


class HandleRequest(object):

    def __init__(self):
        """
        初始化session对象以及headers
        """
        self.login_user = {"userCode": 'admin', "password": '1'}
        logger.debug(f"初始化[{self.__init__.__name__}]方法")
        self.session = requests.Session()
        logger.debug(f"创建[session]对象{self.session}")
        self.headers = self.session.headers
        logger.debug(f"初始化请求头[headers]{self.headers}")

    def __login(self):
        """
        登录授权认证
        :return:
        """
        logger.info(f"尝试登录,调用[{self.__login.__name__}]方法")
        self.session.headers.update({'Content-Type': 'application/json;charset=UTF-8'})
        self.login_user['password'] = self.md5(self.login_user['password'])
        login_response = self.session.post(login_url, json=self.login_user)
        # print(login_response.cookies.values())
        if login_response.json()["code"] == 0:
            Authorization = ''.join(['Basic ', login_response.json()['result']])
            self.session.headers.update({'Authorization': Authorization})
            logger.info(f"获取登录令牌:{self.session.cookies}")

            # 返回0表示登录成功
            return 0
        elif login_response.json()["code"] == 11000:
            # 登录失败
            logger.info(f"{login_response.json()['message']}")
            logger.debug("登录失败")
            # 返回11000表示登录失败
            return 11000

    def md5(self, password):
        """
        对密码进行md5加密处理
        :return:
        """
        md = hashlib.md5()
        md.update(password.encode("utf-8"))
        password = md.hexdigest()
        return password

    def __connection(self, method, url, data, headers, n):
        if n <= 3:
            num = 5
            while num >= 1:
                logger.info(f"{num}秒后，开始尝试第{n}次连接")
                time.sleep(1)
                num -= 1
            return self.request(method, url, data, headers, n=n + 1)
        else:
            logger.info("结束向http连接，请查看连接是否正确")

    def __if_token(self, method, url, data, headers, res):
        if 'Message' in res.json():
            if res.json()["Message"] == 'logout':
                # 判断是否登录
                code = self.__login()
                if code == 0:
                    res = self.request(method, url, data, headers)
        elif 'code' in res.json():
            if res.json()['code'] == 10028:
                code = self.__login()
                if code == 0:
                    res = self.request(method, url, data, headers)
            elif res.json()['code'] == 5000:
                # 增加code码为5000错误，表示token错误
                code = self.__login()
                if code == 0:
                    res = self.request(method, url, data, headers)
        return res

    def __request(self, method, url, data, headers):
        if method.strip().lower() == 'get':
            res = self.__get(url, data, headers)
        elif method.strip().lower() == 'post':
            res = self.__post(url, data, headers)
        elif method.strip().lower() == 'delete':
            res = self.__delete(url, data, headers)
        elif method.strip().lower() == 'put':
            res = self.__put(url, data, headers)
        else:
            logger.error(f"传入的方法{method.strip().lower()}不正确")
            logger.info("传入的方法不正确")
            return None
        return self.__if_token(method, url, data, headers, res)

    def __get(self, url, data, headers):
        return self.session.get(url, params=data, headers=headers, verify=False)

    def __post(self, url, data, headers):
        return self.session.post(url, json=data, headers=headers, verify=False)

    def __delete(self, url, data, headers):
        return self.session.delete(url, json=data, headers=headers, verify=False)

    def __put(self, url, data, headers):
        return self.session.put(url, json=data, headers=headers, verify=False)

    def request(self, method, url, data=None, headers=None, n=1):
        try:
            res = self.__request(method, url, data, headers)
        except AttributeError as e:
            logger.error("NoneType类型错误")
            logger.error(f"AttributeError,具体异常:{e}")
            raise e
        except Exception as e:
            logger.error("http连接异常")
            logger.error(f"具体异常:{e}")
            # 尝试连接
            res = self.__connection(method, url, data, headers, n)

            raise e
        finally:
            logger.info("释放session资源")
            self.session.close()
            return res


if __name__ == '__main__':
    login = HandleRequest()
    body = {"ID": "", "CREATEDTIME": "", "PlateNo": "", "PlateColor": "2", "InfoType": "01",
            "RegisterDate": "2020-03-04 00:00:00", "UseProperty": "", "Payload": "", "Serialid": "", "VehicleModel": "",
            "HomeArea": "", "VehicleIdentificationNo": "", "OperatorId": "01", "DISABLED": "0", "VehicleType": "",
            "Fuelkind": "", "Busload": "", "OwnerName": "", "VehicleModelRemark": "", "HomeAreaRemark": "",
            "EngineCode": "", "REMARK": "", "PLATENO": "鄂A10111", "PLATETYPE": "02"}

    url = 'http://192.168.0.108:8088/api/SysManage/SpecialVeihcle/Post'
    res_1 = login.request('post', url, data=body)
    print(res_1.json())
