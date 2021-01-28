from src.color_print import *
import requests
import re
from prettytable import PrettyTable
import sys
import nmap
import time


def nmap_assign_port_scan(url, port):           # 仅扫描指定端口
    print_info('扫描端口' + color.green(port.replace(',', ' ')))
    print_info('大约需要' + color.green('1分钟'))
    start_time = time.time()
    port_info_table = PrettyTable(['IP地址', 'MAC地址', '端口号', '状态', '原因', '额外信息', '名字', '版本', '产品', 'CPE', '脚本'])
    nm = nmap.PortScanner()
    scan_raw_result = nm.scan(hosts=url, arguments='-p ' + port)
    end_time = time.time()
    for host, result in scan_raw_result['scan'].items():
        if result['status']['state'] == 'up':
            port_info_list = []
            # print_info('扫描' + result['addresses']['ipv4'])
            # print_info('MAC地址' + result['addresses']['mac'])
            try:
                for port in result['tcp']:
                    try:
                        port_info_list.append(result['addresses']['ipv4'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['addresses']['mac'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(str(port))
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['state'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['reason'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['extrainfo'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['name'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['version'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['product'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['cpe'])
                    except:
                        port_info_list.append('None')
                    try:
                        port_info_list.append(result['tcp'][port]['script'])
                    except:
                        port_info_list.append('None')
                    port_info_table.add_row(port_info_list)
                    port_info_list = []
            except:
                pass
    print(port_info_table)
    print_info('扫描用时' + color.green(str(round(end_time - start_time, 2))) + color.green('秒'))
