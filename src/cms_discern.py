from src.color_print import *
from src.get_user_agent import *
import requests
import subprocess
import re
from prettytable import PrettyTable
import sys


def cms_discern(target_url, write=False, output=None):
    cms_discern_table = PrettyTable(['Searching', 'Result'])
    print_info('正在识别CMS')
    url = 'http://whatweb.bugscaner.com/what.go/'
    result_url = url + target_url
    data = {
        'url': target_url,
        'location_capcha': 'no'
    }
    referer = 'http://whatweb.bugscaner.com/look/'
    response = requests.post(url, data=data, headers=get_user_agent()).text
    # print(response)
    json_data = eval(response)
    # print(json_data)
    if write == False:
        for key, value in json_data.items():
            cms_discern_table.add_row([key, value])
            # print(key, value)
        print(cms_discern_table)
        
    else:
        f = open(output, 'w')
        f.write(target_url + '\n\n')
        for key, value in json_data.items():
            f.write(str(key) + '       ' + str(value) + '\n')
        print_info('成功获取CMS指纹信息')
        print_info('保存路径为 ' + color.yellow(output))
        f.close()


def whatweb_cms(url, output=None):
    command_str = 'whatweb -a 3 -v ' + url
    if output == None:
        print_info('调用whatweb检测')
        print_info(command_str)
        command = command_str.split(' ')
        rsp = subprocess.Popen(command)
        rsp.communicate()
        print(rsp)
    else:
        command = command_str.split(' ')
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait()
        out = p.stdout.read().decode()
        try:
            with open(output, 'w+') as fp:
                fp.write(out)
            print_info('whatweb成功获取CMS指纹信息')
            print_info('保存路径为 ' + color.yellow(output))
        except:
            print_error('输入的文件名错误')