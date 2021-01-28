import ftplib
import time
from src.color_print import *
from multiprocessing import Pool
import ipaddress
from tqdm import tqdm
import sys
from prettytable import PrettyTable

def ftp_weak_passwd(ip, username, DICT='./passwd_dict/dict.txt', threads=10):
    user_pass_table = PrettyTable(['用户名', '密码'])
    try:
        password_list = open(DICT, 'r').readlines()
    except:
        print_error('密码字典路径错误')
    ip_user_passwd = []
    for i in range(len(password_list)):
        pwd = password_list[i].strip()
        ip_user_passwd.append((ip, username, pwd))
    # print(ip_user_passwd)
    # print(threads)
    print_info('使用' + color.green(str(threads)) + '个线程')
    try:
        with Pool(threads) as p:
            pool_result = list(
                tqdm(p.imap(ftp_login, ip_user_passwd), total=len(ip_user_passwd)))
    except:
        pass
    for result in pool_result:
        if result[0] == 1:
            print_info(color.green(ip) + '存在FTP弱口令')
            user_pass_table.add_row([result[1], result[2]])
            print(user_pass_table)
            break
        

def ftp_login(option):
    if len(option) != 3:
        print_error('参数错误')
        exit(0)
    ip = option[0]
    username = option[1]
    passwd = option[2]
    try:
        port = 21
        ftp = ftplib.FTP()
        ftp.connect(ip, port, 10)
        ftp.login(username, passwd)
        ftp.quit()
        return (1, username, passwd)
    except:
        return (0, username, passwd)


def ftp_anonymous_enable(ip, port=21):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port, 10)
        ftp.login()
        return (1, ip)
    except:
        return (0, ip)


def network_ftp_anonymous_enable(network, threads=10, port=21):
    net_list = []
    print_info('对网段' + network + '进行FTP匿名登录检测')
    ip_list = ipaddress.ip_network(network)
    for ip in ip_list:
        net_list.append((str(ip)))
    print_info('使用' + str(threads) + '个线程')
    # print(net_list)
    try:
        with Pool(threads) as p:
            pool_result = list(tqdm(p.imap(ftp_anonymous_enable, net_list), total=len(net_list)))
    except:
        pass
    for info in pool_result:
        if info[0] == 1:
            print_info(info[1] + '开启了FTP匿名登录')


if __name__ == '__main__':
    network_ftp_anonymous_enable('192.168.2.0/24')
