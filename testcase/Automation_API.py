import ast
import unittest
from collections import ChainMap

import ddt
import requests

from lib.Seach_json import GetKeyValue
from lib.readexcel import ReadExcel
from lib.runmethod import Runmethod
from config import setting
from lib.GetData import GetData
from lib.depend_data import DependentData
from lib.writeexcel import WriteExcel
from lib.jsonutils import OperationJson

# 读取表格数据
testData = ReadExcel(setting.SOURCE_FILE, "Sheet1").read_data()
# 判断是否需要执行
testdata = []
for row in range(0, len(testData)):
    if testData[row]['execute'] == 'yes' or testData[row]['execute'] == 'Yes':
        testdata.append(testData[row])


@ddt.ddt
class Automation_API(unittest.TestCase):

    # 初始化操作
    def setUp(self):
        # 模拟请求对象
        self.run_method = Runmethod()
        # 获取数据对象
        self.Getdata = GetData()
        self.data = self.Getdata.get_data()
        # 存储用例返回结果
        self.request_datas = {}
        # 存储依赖用例id
        self.depend_id = []
        print("test begin...")
        # 保持会话
        self.s = requests.session()
        # 获取token
        self.sys_login()

    # 运行结束操作
    def tearDown(self):
        print("test end...")

    # 获取token
    def sys_login(self):
        # 每次执行登录操作
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Content-Type": "application/json"}
        login_url = "http://192.168.1.19/sso/getToken"
        data = {"userName": "ceshi88", "password": "123456", "userType": "4"}
        login_res = requests.post(url=login_url, json=data, headers=header)
        login_result = login_res.json()
        if login_result['code'] == 0:
            print("登录http://192.168.1.19" + "成功\n" + "userName=ceshi88\nuserType=4")
        else:
            print("登录http://192.168.1.19" + "失败")
        ut = login_result['data']
        # requests.utils.add_dict_to_cookiejar(self.s.cookies, {'token': ut_result['data']['token'],
        #                                                    'Bearer': ut_result['data']['tokenType'], 'gjpt': 'js'})
        # print("存储cookie成功")
        header_add = {'Authorization': ut}
        header.update(header_add)
        self.s.headers = header
        # print(self.data)

    def execute_depend(self, r, data, params):
        # 存储用例request和params
        request_data = data
        params = params
        depend_id = []
        # 定义循环开始下标
        begin_index = 0
        # 存储用例行
        rn = r - 1
        # 存储依赖发送数据
        depend_body = {}
        depend_params = ""
        # 获得依赖用例data对象
        # 获取依赖用例id
        depent_case_list = ast.literal_eval(data[rn]['dependent_case'])
        depent_case_key = []
        depent_case_value = []
        for key, value in depent_case_list.items():
            depent_case_key.append(key)
            depent_case_value.append(value)
        for k in range(0, len(depent_case_key)):
            dependdata = DependentData(case_id=depent_case_key[k])
            depend_id.append(dependdata.case_id)
            print("执行依赖接口，接口id：" + dependdata.case_id)
            # 判断是否需要嵌套依赖用例
            # 依赖用例的依赖行号
            depent_row = dependdata.opera_excel.get_row_num(dependdata.case_id)
            if data[depent_row - 1]['dependent_case'] != "":
                self.execute_depend(depent_row, request_data, params)
            depend_response_data = dependdata.get_data_for_key(self.s, row=rn + 1)
            # 获取依赖的key，并转换成list
            depend_key = list(data[rn]['dependent_field'].split(","))
            # 获取发送依赖的value类型
            depend_body_type = list(data[rn]['depend_field_type'].split(","))
            # 判断依赖返回值发送类型，body添加body，params添加params
            # print(depend_reponse_data)
            # print(depend_key)
            # print(depend_body_type)
            # print(self.request_data)
            if data[rn]['depend_type'] == 'body':
                # 将依赖key和返回值获取关键字value组成字典
                for b in range(begin_index, depent_case_value[k]):
                    if depend_body_type[b] == "str":
                        depend_body[depend_key[b]] = depend_response_data[b]
                    elif depend_body_type[b] == "list":
                        depend_body[depend_key[b]] = list(depend_response_data[b].split(","))
                if request_data == "":
                    request_data = depend_body
                else:
                    request_data = dict(ChainMap(request_data, depend_body))
            elif data[rn]['depend_type'] == 'params':
                # 将依赖key和返回值获取关键字value组成参数形式
                for p in range(begin_index, depent_case_value[k]):
                    depend_params += "&" + depend_key[p] + "=" + depend_response_data[p]
                params += depend_params
            begin_index = depent_case_value[k]
            # print(self.request_data)
            # print(self.params)
            print("依赖执行完成")

    # 测试规程方法
    @ddt.data(*testdata)
    def test_api(self, data):
        # 获得用例data对象
        case = DependentData(case_id=data['ID'])
        # 根据ID获取所在行
        rowNum = case.opera_excel.get_row_num(case.case_id)
        if data['body'] != "":
            # 获取body
            self.request_data = OperationJson().get_data(data['body'])
        else:
            self.request_data = ""
        # 获取params
        self.params = "?" + data['params']
        # 获取body类型
        body_type = data['type']
        # 判断是否需要依赖用例
        if data['dependent_case'] != "":
            self.execute_depend(rowNum, self.request_data, self.params)

        # 将headers字符串转换成字典
        headers = self.s.headers
        if data['headers'] != "":
            headers = headers.update(ast.literal_eval(data['headers']))

        # 打印本次测试用例情况
        print("******* 正在执行用例 ->{0} *********".format(data['ID']))
        print("请求方式: {0}\n请求URL: {1}".format(data['method'], data['url']))
        print("请求参数: {0}".format(self.params))
        print("post请求body类型为：{0} \nbody内容为：{1}".format(body_type, self.request_data))

        # 发送接口请求，存储json结果
        if self.params != "?":
            res = self.run_method.run_main(self.s, method=data['method'], url=data['url'] + self.params,
                                           data=self.request_data, header=headers, body_type=body_type)
        else:
            res = self.run_method.run_main(self.s, method=data['method'], url=data['url'], data=self.request_data,
                                           header=headers, body_type=body_type)

        # expect转换成字典
        expect = ast.literal_eval(data['expect'])

        # 从响应json中递归查询
        # gkv = GetKeyValue(o={'demo': 'show demo'}, mode='j')  # mode=j意味传入的object是一个json对象
        gkv = GetKeyValue(res, mode='s')  # mode=s意味着传入的object是一个json的字符串对象
        # 储存key
        key_list = list(expect.keys())
        # 根据key存储所有返回中对应的value
        expect_list = []
        for i in range(0, len(key_list)):
            expect_list.append(gkv.search_key(key_list[i]))

        # 结果标识
        flag = False
        # unittest断言对比结果
        # 循环expect字典长度次数
        for key in range(0, len(key_list)):
            # 判断expect中value是否在result中
            self.assertIn(expect[key_list[key]], expect_list[key])
            if expect[key_list[key]] in expect_list[key]:
                print("期待结果" + str(key + 1) + "-->" + str(expect[key_list[key]]) + "-->在返回结果中存在")
                flag = True
            else:
                print("期待结果" + str(key + 1) + "-->" + str(expect[key_list[key]]) + "-->在返回结果中不存在")
                flag = False

        if flag:
            print("接口测试通过")
            WriteExcel(setting.TARGET_FILE).write_data(row_n=rowNum + 1, value='PASS')
            print("-----------------------------------------------------------------------------")
        else:
            print("接口测试失败")
            WriteExcel(setting.TARGET_FILE).write_data(row_n=rowNum + 1, value='FAIL')
            print("-----------------------------------------------------------------------------")


if __name__ == '__main__':
    unittest.main()
