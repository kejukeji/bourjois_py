# coding: UTF-8

def get_from_element(form, param):
    '''获取表单元素'''
    dic = {}
    for p in param:
        form_result = form.get(p)
        dic[p] = form_result # key为model中的列，值为从form表单中得到的value
    return dic
