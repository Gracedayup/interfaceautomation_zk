import configparser
from common import project_path
import os

class HandleConfig:

    def __init__(self):
        #初始化
        self.cf=configparser.ConfigParser()
        self.config_dir = project_path.config_dir

    def get_value(self,filename,section,option):
        config_name = os.path.join(self.config_dir, filename)

        self.cf.read(config_name,encoding="utf-8")#调用read函数打开文件
        #获取数据
        try:
            value=self.cf.get(section,option)
        except Exception as e:
            print("输入的区域或者选项错误")
            raise e
        return value
#eval()
if __name__ == '__main__':
    config_name = 'special_vehicle.ini'
    workbook_name = eval(HandleConfig().get_value(config_name, 'excel', 'file_name'))
    print("获取到的值是：{0}".format(workbook_name))


