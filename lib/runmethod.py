# coding:utf-8
# 使用Request 库 模拟发送请求
import json




class Runmethod:

    # 定义方法  判断返回的数据是否是json数据
    @staticmethod
    def check_json_format(raw_msg):
        # 判断是否是字符串
        if isinstance(raw_msg, str):
            try:
                # 如果不是json  报异常
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False

    # 模拟的是POST请求  目标获取结果

    def post_main(self, s, url, data, header, body_type):
        if body_type == "json":
            data_json = json.dumps(data)
            res = s.post(url=url, data=data_json, headers=header)
        else:
            res = s.post(url=url, data=data)

        if self.check_json_format(res.text):
            # 如果返回的数据是json数据
            print("实际响应结果", res.json())
            return res.json()
        else:
            print("实际响应结果", res.text)
            return res.text

    # 模拟get请求
    def get_main(self, s, url, data, header, body_type):
        if body_type == "json":
            data_json = json.dumps(data)
            res = s.get(url=url, data=data_json, headers=header, verify=False)
        else:
            res = s.get(url=url, data=data, verify=False)

        if self.check_json_format(res.text):
            # 如果返回的数据是json数据
            print("实际响应结果", res.json())
            return res.json()
        else:
            print("实际响应结果", res.text)
            return res.text

        # 合并两个方法的调用
    def run_main(self, s, method, url, data, header, body_type):
        if method == "Post" or method == "post":
            res = self.post_main(s, url, data, header, body_type)
        else:
            res = self.get_main(s, url, data, header, body_type)
            # 以json结果返回数据
        return json.dumps(res, ensure_ascii=False, sort_keys=True, indent=2)
