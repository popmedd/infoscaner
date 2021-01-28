import argparse
import nmap
from colorama import init, Fore, Back, Style
import time
from prettytable import PrettyTable
import requests
import re
import os
import sys
import subprocess
from tqdm import tqdm, trange
from multiprocessing.dummy import Pool
import math
import threading
from src.ssh_connect import ssh_connect
import multiprocessing
from src.whois import *
from src.subdomain_crawl import *
from src.c_segment import *
from src.nmap_all_scan import *
from src.nmap_assign_port_scan import *
from src.nmap_assign_port_scan_alive import *
from src.icp_search import *
from src.nslookup import *
from src.cms_discern import *
from src.dir_scan import *
from src.ssh_root_passwd_crack import *
from src.get_user_agent import *
from src.ftp_connect import *
from src.nmap_ip_infomation import nmap_ip_infomation
from src.nmap_dns_brute import nmap_dns_brute
from src.nmap_http_head import nmap_http_head
from src.subdomain_brute import *
from src.config import *
from src.waf_check import *
from src.dir_crawl import *


if __name__ == '__main__':
    print_msg()
    parser = argparse.ArgumentParser("python3 infoscanner.py")
    parser.add_argument('-u', '--url', help='指定目标url或者搜索的目标 | (默认扫描域名)', required=True, type=str)
    parser.add_argument('-w', '--whois', help="WHOIS信息 | 域名", action="store_true")
    parser.add_argument('-N', '--nei', help="C段和旁站信息 | 域名", action="store_true")
    parser.add_argument('-C', '--cms', help="CMS指纹信息 | 域名", action="store_true")
    parser.add_argument('-i', '--icp', help="ICP备案号查询 | 域名", action="store_true")
    parser.add_argument('-n', '--nslookup', help="Nslookup | 域名", action="store_true")
    parser.add_argument('-W', '--Waf', help="Waf检测 | 域名", action="store_true")
    parser.add_argument('-y', '--anonymous', help="检测匿名登录", action="store_true")
    parser.add_argument('-s', '--subdomain', help="子域名爆破 | 域名文件位置", action="store_true")
    parser.add_argument('-a', '--all', help='全面扫描 | ip', action="store_true")
    parser.add_argument('-p', '--port', help='指定端口扫描(21,22,80,8080) | ip扫描时指定端口', type=str)
    parser.add_argument('-l', '--live', help="仅扫描开启该端口的主机 | ip", action="store_true")
    parser.add_argument('-d', '--dirtype', help="目录爆破(扫描类型) | ip或域名", type=str)
    parser.add_argument('-D', '--Dircrawl', help="目录爬取(crawlergo) | ip或域名", action="store_true")
    parser.add_argument('-c', '--cookie', help='目录爆破或扫描时指定cookie | 默认为None', type=str)
    parser.add_argument('-t', '--threads', help="线程数量 | 扫描", type=str, default='10')
    parser.add_argument('-o', '--output', help="输出结果 | 查询结果输出", type=str)
    args = parser.parse_args()
    url = args.url
    port = args.port
    whois = args.whois
    Alive = args.live
    anonymous = args.anonymous
    Dir_crawl = args.Dircrawl
    neigh = args.nei
    output = args.output
    threads = args.threads
    dirtype = args.dirtype
    waf = args.Waf
    nmap_ip = args.all
    cms = args.cms
    icp = args.icp
    nslookup = args.nslookup
    cookie = args.cookie
    all_scan = args.all
    subdomain = args.subdomain
    # print(args)
    if url == None:
        print_msg()
    elif url != None and port == None and Dir_crawl == False and waf == False and threads == '10' and anonymous == False and nslookup == False and icp == False and dirtype == None and Alive == False and cms == False and output == None and nmap_ip == False and cookie == None and all_scan == False and subdomain == False and neigh == False:  # 默认扫描
        if url.startswith('http://'):
            tmp_url = url.replace('http://', '')
            url = tmp_url
        if url.startswith('https://'):
            tmp_url = url.replace('https://', '')
            url = tmp_url
        if url.endswith('/'):
            url = url[:-1]
        try:
            print_info('尝试从www.aizhan.com获取的whois信息')   # aizhan whois查询
            chinaz_whois_search(url)
        except:
            print_error('无法从www.aizhan.com获取的whois信息')
        try:
            print_info('尝试从who.is获取的whois信息')              # who.is whois查询
            who_is_whois_search(url)
        except:
            print_error('无法从who.is获取的whois信息')
        python_whois_search(url=url)
    elif url != None and port == None and Dir_crawl == False and threads == '10' and waf == False and anonymous == False and nslookup == False and icp == False and dirtype == None and Alive == False and cms == False and output != None and nmap_ip == False and cookie == None and all_scan == False and subdomain == False and neigh == False:  # 默认扫描并输出
        if url.startswith('http://'):
            tmp_url = url.replace('http://', '')
            url = tmp_url
        if url.startswith('https://'):
            tmp_url = url.replace('https://', '')
            url = tmp_url
        if url.endswith('/'):
            url = url[:-1]
        try:
            print_info('尝试从www.aizhan.com获取的whois信息并保存')      # aizhan whois查询
            chinaz_whois_search(url, write=True, output=output)
        except:
            print_error('无法从www.aizhan.com获取的whois信息')
        try:
            print_info('尝试从who.is获取的whois信息并保存')              # who.is whois查询
            who_is_whois_search(url, write=True, output=output)
        except Exception:
            print_error('无法从who.is获取的whois信息')
        python_whois_search(url=url, output=output)
    elif url != None and all_scan == True:                        # 全面扫描
        try:
            nmap_all_scan(url)
        except:
            print_error('全面扫描失败')
    elif url != None and port != None and Alive == False:          # 端口扫描
        try:
            nmap_assign_port_scan(url, port)
        except:
            print_error('扫描失败')
    elif url != None and port != None and Alive == True:            # 存活端口扫描
        try:
            nmap_assign_port_scan_alive(url, port)
        except:
            print_error('扫描失败')
    elif url != None and neigh == True and output == None:          # C段和旁站扫描
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            c_segment_search(url)
        except:
            print_error('扫描失败')
    elif url != None and neigh == True and output != None:          # C段和旁站扫描并保存
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            c_segment_search(url, write=True, output=output)
        except:
            print_error('扫描失败')
    elif url != None and cms == True and output == None:                                # CMS指纹探测
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            cms_discern(url)
        except:
            print_error('扫描失败')
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            whatweb_cms(url)
        except:
            print_error('whatweb扫描失败')
    elif url != None and cms == True and output != None:                                # CMS指纹探测并输出
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            cms_discern(url, write=True, output=output)
        except:
            print_error('扫描失败')
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            whatweb_cms(url, output=output)
        except:
            print_error('whatweb扫描失败')
    elif url != None and icp == True and output == None:                                # ICP查询
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            icp_search(url)
        except:
            print_error('从icp.aizhan.com获取信息失败')
        try:
            chinaz_icp_search(url)
        except:
            print_error('从icp.chinaz.com获取信息失败')
    elif url != None and icp == True and output != None:                                # ICP查询并保存
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            icp_search(url, write=True, output=output)
        except:
            print_error('扫描失败')
        try:
            chinaz_icp_search(url, output=output)
        except:
            print_error('从icp.chinaz.com获取信息失败')
    elif url != None and nslookup == True and output == None:                                # NSLOOKUP查询
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            nslookup_search(url)
        except:
            print_error('扫描失败')
    elif url != None and nslookup == True and output != None:                                # NSLOOKUP查询并保存
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
            nslookup_search(url, write=True, output=output)
        except:
            print_error('扫描失败')
    elif url != None and dirtype != None:                                       # 目录扫描
        if int(threads) < 1:
            print_error('线程数不能小于1')
            exit(0)
        multi_dir_scan_all(url, threads, dirtype, cookie)
    elif url != None and waf == True and output == None:            # waf检测
        waf_check(url)
    elif url != None and waf == True and output != None:            # waf检测输出
        waf_check(url, output=output)
    elif url != None and subdomain == True and output == None:     # 子域名爆破
        # print(url)
        print_subdomain(url)
    elif url != None and subdomain == True and output != None:      # 子域名爆破并写入
        write_subdomain(url, output)
    elif url != None and anonymous == True and output == None:      # FTP匿名登录检测
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
        except:
            print_error('请检查您的-u参数')
        if url[-2] == '/' or url[-3] == '/':        # 输入为网段的情况
            network_ftp_anonymous_enable(url, threads=int(threads))
        else:                                       # 输入不是网段的情况
            ftp_anonymous_result = ftp_anonymous_enable(url)
            if (ftp_anonymous_result[0] == 1):
                print_info('目标开启了FTP匿名登录')
            else:
                print_info('目标未开启匿名登录')
    elif url != None and anonymous == True and output != None:      # FTP匿名登录检测输出
        print_info('该命令暂不支持输出')
        try:
            if url.startswith('http://'):
                tmp_url = url.replace('http://', '')
                url = tmp_url
            if url.startswith('https://'):
                tmp_url = url.replace('https://', '')
                url = tmp_url
            if url.endswith('/'):
                url = url[:-1]
        except:
            print_error('请检查您的-u参数')
        if url[-2] == '/' or url[-3] == '/':        # 输入为网段的情况
            network_ftp_anonymous_enable(url, threads=int(threads))
        else:                                       # 输入不是网段的情况
            ftp_anonymous_result = ftp_anonymous_enable(url)
            if (ftp_anonymous_result[0] == 1):
                print_info('目标开启了FTP匿名登录')
            else:
                print_info('目标未开启匿名登录')
    elif Dir_crawl == True and output == None:      # 目录爬取
        url_list = get_dir()
        url_table = PrettyTable(['目录'])
        for url in url_list:
            url_table.add_row([url])
        print(url_table)
    elif Dir_crawl == True and output != None:      # 目录爬取并输出
        url_list = get_dir()
        if os.path.exists(output):
            choice = print_input('文件已经存在 是否覆盖[y/n] ')
            if choice == 'y' or choice == 'Y' or choice == 'yes' or choice == 'YES' or choice == '是':
                f = open(output, 'w')
                for url in url_list:
                    f.write(url + '\n')
                f.close()
                print_info('写入完成')
                print_info('写入路径为' + output)
            else:
                print_info('不覆盖目标文件')
                print_info('请重新选择目标文件')
                exit(0)
        else:
            f = open(output, 'w')
            for url in url_list:
                f.write(url + '\n')
            f.close()
            print_info('写入完成')
            print_info('写入路径为' + output)
    else:                                                     # 参数有误
        rsp_two = subprocess.Popen(['python3', 'infoscaner.py', '-h'])
        rsp_two.communicate()
