class Globalvar:
    # 定义全局变量与excel的对应关系

    Id = '1'  # ID
    request_name = '2'  # UseCase
    url = '3'  # url
    request_way = '4'  # method
    header = '5'  # header
    params = '6'  # params
    data = '7'  # body
    type = '8'  # type
    case_depend = '9'  # dependent_case
    data_depend = '10'  # dependent_response
    field_depend = '11'  # dependent_field
    run = '14'  # execute
    expect = '15'  # expect
    result = '16'  # result
    tester = '17'  # tester


# 对外提供获取方法

# 获取caseid


def get_id():
    return Globalvar.Id


# 获取url


def get_url():
    return Globalvar.url


def get_run():
    return Globalvar.run


def get_run_way():
    return Globalvar.request_way


def get_header():
    return Globalvar.header


def get_case_depend():
    return Globalvar.case_depend


def get_data_depend():
    return Globalvar.data_depend


def get_data_params():
    return Globalvar.params


def get_field_depend():
    return Globalvar.field_depend


def get_data():
    return Globalvar.data


def get_result():
    return Globalvar.result


def get_header_value():
    return Globalvar.header


def get_tester():
    return Globalvar.tester


def get_type():
    return Globalvar.type


def get_expect():
    return Globalvar.expect
