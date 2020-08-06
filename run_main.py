import unittest
from config import setting
import time
from lib.HTMLTestRunner import HTMLTestRunner
from lib.newReport import new_report
from database import test_data
from lib.sendmail import send_mail


def creatsuite():
    # ---将用例添加到测试套件---
    testunit = unittest.TestSuite()
    # 加载TEST_CASE指向用例文件
    test_dir = setting.TEST_CASE
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*API.py')
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTest(test_case)
            print(testunit)
    return testunit


def run_test(case_suite):
    # 初始化数据库
    # test_data.init_data()
    current_time = time.strftime("%Y-%m-%d-%H-%M")
    # 获取报告存放路径
    report_dir = setting.TEST_REPORT
    # 设定报告名称
    report_file = report_dir + '/' +current_time + "-Test_Result.html"
    report_stream = open(report_file, "wb")
    # 设定HTMLTestRunner报告标题及摘要及存放路径
    runner = HTMLTestRunner(stream=report_stream, title=current_time + "接口自动化测试报告",
                            description="环境：windows 10 浏览器：chrome", tester='田晨旭')
    # 运行测试
    runner.run(case_suite)
    report_stream.close()
    report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
    # 发送邮件
    # send_mail(report)


if __name__ == '__main__':
    case_suite = creatsuite()
    run_test(case_suite)
