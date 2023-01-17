'''
Author: Crange 839704627@qq.com
Date: 2023-01-13 15:03:14
LastEditors: Crange 839704627@qq.com
LastEditTime: 2023-01-17 20:50:39
'''
import configparser as cp

def update_ini(themestyle='darkly'):
    conf = cp.ConfigParser()
    conf.read('./conf.ini')
    conf.set('config', 'themesname', themestyle)

    with open('./conf.ini', 'w') as fw:
        conf.write(fw)

def load_ini():
    conf = cp.ConfigParser()
    conf.read('./conf.ini')
    cur_style = conf.get('config', 'themesname')
    return cur_style.__str__()