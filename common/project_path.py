import os
#项目的目录
current_dir = os.path.dirname(os.path.dirname(__file__))


testData_dir = os.path.join(current_dir,'test_data')#测试数据的路径

testCase_dir = os.path.join(current_dir,'test_case')#测试用例的路径

config_dir = os.path.join(current_dir,'config')#配置文件的路径

log_dir = os.path.join(current_dir,'logs')#日志存在的路径

report_dir = os.path.join(current_dir,'test_report')#测试报告的路径







