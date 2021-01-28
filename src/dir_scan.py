import requests
from multiprocessing import Queue, Pool
import threading
import sys
from src.color_print import *
import requests
import re
from prettytable import PrettyTable
from tqdm import tqdm
from src.get_user_agent import *


def multi_dir_scan_all(url, threads, dirtype, cookie):
    print_info('对' + url + '进行目录扫描')
    if url.startswith('http://'):
        url = url
    elif url.startswith('https://'):
        tmp_url = url.replace('https://', 'http://')
        url = tmp_url
    else:
        url = 'http://' + url
    scan_result_table = PrettyTable(['网站目录', '状态码'])
    print_info('扫描' + dirtype + '类型的文件')
    if dirtype == 'dir':
        dir_txt = open("./dir_dict/DIR.txt").readlines()
        all_url = dir_txt
    elif dirtype == 'php':
        php_txt = open("./dir_dict/PHP.txt").readlines()
        all_url = php_txt
    elif dirtype == 'asp':
        asp_txt = open("./dir_dict/ASP.txt").readlines()
        asp_two_txt = open("./dir_dict/ASP_TWO.txt").readlines()
        all_url = asp_txt + asp_two_txt
    elif dirtype == 'jsp':
        jsp_txt = open("./dir_dict/JSP.txt").readlines()
        all_url = jsp_txt
    elif dirtype == 'mdb':
        mdb_txt = open("./dir_dict/MDB.txt").readlines()
        all_url = mdb_txt
    else:
        php_txt = open("./dir_dict/PHP.txt").readlines()
        asp_txt = open("./dir_dict/ASP.txt").readlines()
        jsp_txt = open("./dir_dict/JSP.txt").readlines()
        mdb_txt = open("./dir_dict/MDB.txt").readlines()
        dir_txt = open("./dir_dict/DIR.txt").readlines()
        asp_two_txt = open("./dir_dict/ASP_TWO.txt").readlines()
        all_url = php_txt + asp_txt + jsp_txt + mdb_txt + asp_two_txt + dir_txt
    # all_url = ['/robots.txt', '/index.html']
    scan_url_list = []
    for line in all_url:
        if line.startswith('/'):
            scan_url = url + line.strip()
        else:
            scan_url = url + '/' + line.strip()
        if cookie == None:
            headers = get_user_agent()
        else:
            headers = get_user_agent()
            headers['Cookie'] = cookie
        scan_url_list.append((scan_url, headers))
    # print(scan_url_list[:5])
    thread_count = int(threads)
    print_info('对' + color.green(url) + color.green('目录进行全面扫描'))
    print_info('启用' + color.green(str(thread_count)) + color.green('个线程'))
    with Pool(thread_count) as p:
        pool_result = list(tqdm(p.imap(dir_alive_url, scan_url_list), total=len(scan_url_list)))
    for result in pool_result:
        if result[0] == 1:
            scan_result_table.add_row([result[1], result[2]])
    print_info(color.green('扫描的网址是') + color.yellow(url))
    print(scan_result_table)


def dir_alive_url(option):
    dir = option[0]
    header = option[1]
    r = requests.get(dir, headers=header).status_code
    if r == 200:
        return (1, dir, r)
    else:
        return (0, dir, r)


if __name__ == "__main__":
    multi_dir_scan_all('http://localhost')
