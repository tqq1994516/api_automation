# coding:utf-8
import json
from config import setting


class OperationJson:
    # 初始化步骤
    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = setting.TEST_JSON
        else:
            self .file_path = file_path
        self.data = self.read_json()

    # 读取json文件
    def read_json(self):
        # with结构---自动关闭文件
        with open(self.file_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            return data

    # 根据关键字key 获取对应的json数据
    def get_data(self, key):
        return self.data[key]
    # 写入数据到json文件  ---覆盖写

    def write_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as fp:
            # 将json数据写入内容
            fp.write(json.dumps(data, ensure_ascii=False))

    # 追加写---思考: 传入的键  ，json 已经存在 则覆盖原有的内容
    def write_appednd_data(self, data):
        # 将json 中数据遍历  是否传入的键
        with open(self.file_path, 'r', encoding='utf-8') as fp:
            # model已经存在的数据
            model = json.load(fp)
            for i in data:
                # 如果是新的键  追加
                # 如果是存在键 覆盖
                model[i] = data[i]

            # 将model重新转换为json
            jsobj = json.dumps(model, ensure_ascii=False)
        with open(self.file_path, 'w', encoding='utf-8') as fp:
            fp.write(jsobj)


if __name__ == "__main__":
    opjson = OperationJson()
    opjson.write_appednd_data({"name": "zq1"})
    opjson.write_appednd_data({"animals": [{"aname": "zqa1", "banem": "zqa2"}]})
