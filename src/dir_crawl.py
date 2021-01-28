import simplejson
import subprocess
import os
from src.config import *
from src.color_print import *
import time


def crawlergo_dir(url):
    url_list = []
    command_str = './crawlergo_linux_amd64/crawlergo -c ' + chrome_path + ' -o json ' + url
    print_info('使用crawlergo爬取url')
    print_info(command_str)
    command = command_str.split(' ')
    rsp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = rsp.communicate()
	#  "--[Mission Complete]--"  是任务结束的分隔字符串
    # print(output.decode())
    
    result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
    # print(result)
    req_list = result["req_list"]
    for req in req_list:
        # print(req['url'])
        url_list.append(req['url'])

    # print(url_list)
    return url_list


def rad_dir(url):
    if os.path.exists(rad_json_output_file):
        os.remove(rad_json_output_file)
    url_list = []
    string = ''
    command_str = './rad_linux_amd64/rad_linux_amd64 -t ' + url + ' --json-output ' + rad_json_output_file
    print_info('使用radium爬取url')
    print_info(command_str)
    command = command_str.split(' ')
    rsp = subprocess.Popen(command)
    rsp.communicate()
    f = open(rad_json_output_file, 'r').readlines()
    for i in f:
        string += i
    result = eval(string)
    for json in result:
        try:
            url_list.append(json['URL'])
        except:
            pass
    return url_list
    
    
def get_dir():
    url_list = []
    crawlergo_url_list = crawlergo_dir('http://testphp.vulnweb.com/')
    print_info('crawlergo扫描完成')
    # print(crawlergo_url_list)
    # print(len(crawlergo_url_list))
    rad_url_list = rad_dir('http://testphp.vulnweb.com/')
    print_info('radium扫描完成')
    for rad_url in rad_url_list:
        url_list.append(rad_url)
    for crawlergo_url in crawlergo_url_list:
        url_list.append(crawlergo_url)
    # print(len(rad_url_list))
    result = set(url_list)
    result_list = list(result)
    print_info('去重完成 准备输出')
    # time.sleep(0.2)
    # print(len(result_list))
    
    return result_list
