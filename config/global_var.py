class Globalvar:
    # ����ȫ�ֱ�����excel�Ķ�Ӧ��ϵ

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


# �����ṩ��ȡ����

# ��ȡcaseid


def get_id():
    return Globalvar.Id


# ��ȡurl


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
