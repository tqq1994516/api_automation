# coding:utf-8
import json

from lib.runmethod import Runmethod
from lib.excelutils import OperationExcel
from lib.GetData import GetData
from lib.Seach_json import GetKeyValue


class DependentData:

    # 通过case_id  获取整行的内容
    # 初始化工作
    def __init__(self, case_id):
        self.case_id = case_id
        self.opera_excel = OperationExcel()
        self.data = GetData()

    # 根据caseid 获取出整行的内容
    def get_case_line_data(self):
        rows_data = self.opera_excel.get_rows_data(self.case_id)
        return rows_data

    # 执行依赖用例的测试获取结果
    def run_dependent(self, s):
        run_method = Runmethod()
        # 获取用例行号
        row_num = self.opera_excel.get_row_num(self.case_id)
        # print(row_num)
        method = self.data.get_request_method(row_num)
        # 根据关键字获取json数据
        if self.data.get_request_data(row_num) != None:
            request_data = self.data.get_data_for_json(row_num)
        else:
            request_data = None
        params = self.data.get_params(row_num)
        url = self.data.get_requests_url(row_num)
        header = s.headers
        body_type = self.data.get_type(row_num)
        # print(params)
        if params is not None:
            url_params = url + params
            res = run_method.run_main(s, method=method, url=url_params, data=request_data, header=header,
                                      body_type=body_type)
        else:
            res = run_method.run_main(s, method=method, url=url, data=request_data, header=header, body_type=body_type)
        return res

    # 根据key键 获取响应的内容
    def get_data_for_key(self, s, row):
        # 需求  是从响应的内容response_data中取出 字段 depend_data的键值
        # 推荐 json的解析库   pip install  jsonpath_rw
        # 面临问题 获取 errorcode
        # 获取存储响应数据单元格内容
        depend_data = self.data.get_depend(row)
        # depend_dat字符串转list
        depend_data = list(depend_data.split(","))
        # 获取被依赖用例的响应
        response_data = self.run_dependent(s)
        # 从响应json中递归查询
        # gkv = GetKeyValue(o={'demo': 'show demo'}, mode='j')  # mode=j意味传入的object是一个json对象
        gkv = GetKeyValue(response_data, mode='s')  # mode=s意味着传入的object是一个json的字符串对象
        # 返回查找到的列表
        depend_data_list = []
        for i in range(0, len(depend_data)):
            depend_data_list.append(gkv.search_key(depend_data[i])[0])
        # # depend_data_list内元素若为为list，转str
        # for j in range(0, len(depend_data_list)):
        #     if isinstance(depend_data_list[j], list):
        #         depend_data_list[j] = "".join(depend_data_list[j])
        #     else:
        #         depend_data_list[j] = depend_data_list[j]
        return depend_data_list


        # # 将响应内容写入到depend_data中
        # json_exe = parse(depend_data)
        # # 需求  是从响应的内容response_data中取出 字段 depend_data的键值
        #
        # madle = json_exe.find(response_data)
        #
        # if madle:
        #     return [math.value for math in madle]
