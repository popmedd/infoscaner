import sys
from src.color_print import *
from src.get_user_agent import *
from multiprocessing import Queue, Pool
import requests
import os
from tqdm import tqdm
import subprocess
from prettytable import PrettyTable
from src.config import *

def get_file_content(path):     # 获取扫描子域名目标
    scan_list = []
    try:
        content = open(path, 'r').readlines()
    except:
        print_error('请设置-u参数值为扫描文件位置')
        exit(0)
    for i in content:
        scan_list.append(i.strip())
    return scan_list

def OneForAll_subdomains(target):     # OneForAll扫描的子域名
    oneforall_list = []
    for tar in target:
        command_str = 'python3 ./OneForAll-master/oneforall.py --target ' + tar.strip() + ' run --format result.txt --path ' + OneForAll_output_file
        print_info(color.green("Command:") + color.yellow(command_str))
        command = command_str.split(' ')
        rsp = subprocess.Popen(command)
        rsp.communicate()
        tmp_subdomain_list = open(OneForAll_output_file, 'r').readlines()
        # print(tmp_subdomain_list)
        for tmp_subdomain in tmp_subdomain_list:
            oneforall_list.append(tmp_subdomain.strip())
    return oneforall_list


def sublist3r_subdomains(target):
    sublist3r_list = []
    for tar in target:
        if os.path.exists(sublist3r_output_file):
            os.remove(sublist3r_output_file)
            print_info('删除' + sys.path[0] + sublist3r_output_file)
        command_str = 'python2 ./Sublist3r-master/sublist3r.py -d ' + tar.strip() + ' -o ' + sublist3r_output_file
        print_info(color.green("Command:") + color.yellow(command_str))
        command = command_str.split(' ')
        rsp = subprocess.Popen(command)
        rsp.communicate()
        tmp_subdomain_list = open(sublist3r_output_file, 'r').readlines()
        # print(tmp_subdomain_list)
        for tmp_subdomain in tmp_subdomain_list:
            sublist3r_list.append(tmp_subdomain.strip())
    return sublist3r_list


def request_url(url):           # 判断url是否可以访问
    try:
        r = requests.get(url, headers=get_user_agent()).status_code
        if r == 200:
            return (1, url)
        else:
            return (0, url)
    except:
        return (0, url)


def judge_alive_url(OneForAll_sub_list):            # 判断可访问的域名
    scan_url_list = []
    alive_url = []
    for line in OneForAll_sub_list:
        scan_url = "http://" + line
        scan_url_list.append(scan_url)
    thread_count = 10
    print_info('Use ' + str(thread_count) + ' thread')
    with Pool(10) as p:
        pool_result = list(tqdm(p.imap(request_url, scan_url_list), total=len(scan_url_list)))
    for result in pool_result:
        if result[0] == 1:
            alive_url.append(str(result[1]).replace('http://', ''))
    return alive_url


def subdomain_scan_run(scan_file):
    return_subdomain = []
    tmp_two_subdomain = []
    tmp_subdomain = []
    subdomain = []
    scan_table = PrettyTable(['扫描子域名目标'])
    print_info('扫描文件位置' + scan_file)
    scan_list = get_file_content(scan_file)
    print_info('获取文件内容')
    for scan_subdomain in scan_list:
        print(color.blue(scan_subdomain))
    oneforall_subdomain = OneForAll_subdomains(scan_list)
    sublist3r_domain = sublist3r_subdomains(scan_list)
    # tmp_subdomain.append(oneforall_subdomain)
    # tmp_subdomain.append(sublist3r_domain)
    for sublist3r in sublist3r_domain:
        oneforall_subdomain.append(sublist3r)
    tmp_subdomain = oneforall_subdomain
    for tmp in tmp_subdomain:
        if tmp == '':
            pass
        else:
            tmp_two_subdomain.append(tmp)
    for sub in tmp_two_subdomain:
        if sub not in subdomain:
            subdomain.append(sub)
    for i in subdomain:
        if i == '':
            pass
        else:
            return_subdomain.append(i)
    print_info('扫描完毕')
    remove_file()
    # print(len(return_subdomain))
    return return_subdomain


def remove_file():
    try:
        os.remove('./target/oneforall.txt')
        print_info('删除' + color.yellow(sys.path[0]) + color.yellow('/target/oneforall.txt'))
    except:
        print_error('删除' + sys.path[0] + '/target/oneforall.txt失败')
        pass
    try:
        os.remove('./target/sublist3r.txt')
        print_info('删除' + color.yellow(sys.path[0]) + color.yellow('/target/sublist3r.txt'))
    except:
        print_error('删除' + sys.path[0] + '/target/sublist3r.txt失败')
        pass


def print_subdomain(scan_file):
    subdomain = subdomain_scan_run(scan_file)
    print_info('获取子域名完成')
    print_info('判断可访问的域名')
    alive_subdomain = judge_alive_url(subdomain)
    subdomain_table = PrettyTable(['子域名'])
    for i in alive_subdomain:
        subdomain_table.add_row([i])
    print(subdomain_table)


def write_subdomain(scan_file, path):
    subdomain = subdomain_scan_run(scan_file)
    print_info('获取子域名完成')
    print_info('判断可访问的域名')
    alive_subdomain = judge_alive_url(subdomain)
    file = open(path, 'w')
    for sub in alive_subdomain:
        file.write(sub + '\n')
    file.close()
    print_info('成功将文件写入到' + color.yellow(path))