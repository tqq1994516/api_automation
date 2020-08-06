import os, sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
current_time = time.strftime("%Y-%m-%d-%H-%M")

# 配置文件
TEST_CONFIG = os.path.join(BASE_DIR, "config", "config.ini")
# json文件
TEST_JSON = os.path.join(BASE_DIR, "database", "api_json.json")
# 测试用例模板文件
SOURCE_FILE = os.path.join(BASE_DIR, "database", "APITestCase.xlsx")
# excel测试用例结果文件
TARGET_FILE = os.path.join(BASE_DIR, "report", "excelReport", current_time + "APITestCase.xlsx")
# 测试用例报告
TEST_REPORT = os.path.join(BASE_DIR, "report")
# 测试用例程序文件
TEST_CASE = os.path.join(BASE_DIR, "testcase")
