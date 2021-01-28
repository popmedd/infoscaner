from src.color_print import *
import requests
import re
from prettytable import PrettyTable
import sys
import nmap
import time

def nmap_all_scan(url):
    print_info('进行全面扫描')
    print_info('大约需要' + color.green('3-7分钟'))
    start_time = time.time()
    nm = nmap.PortScanner()
    scan_raw_result = nm.scan(hosts=url, arguments='-A -n -v')
    # print(scan_raw_result)
    end_time = time.time()
    port_info_table = PrettyTable(['IP地址', 'MAC地址', '端口号', '状态', '原因', '额外信息', '名字', '版本'])
    for host, result in scan_raw_result['scan'].items():
        if result['status']['state'] == 'up':
            try:
                print_info("IP地址: " + color.green(result['addresses']['ipv4']))
            except:
                pass
            try:
                print_info("MAC地址: " + color.green(result['addresses']['mac']))
            except:
                pass
            try:
                os_guess_table = PrettyTable(['IP地址', 'MAC地址', '操作系统', '准确度'])
                os_row = []
                for os in result['osmatch']:
                    os_row.append(result['addresses']['ipv4'])
                    os_row.append(result['addresses']['mac'])
                    # print(color.green('操作系统为:') + color.magenta(os['name']) + color.green('    准确度为 ') + color.magenta(os['accuracy']))
                    os_row.append(os['name'])
                    os_row.append(os['accuracy'] + '%')
                    os_guess_table.add_row(os_row)
                print(os_guess_table)
            except:
                pass
            try:
                for port in result['tcp']:
                    if result['tcp'][port]['state'] == 'unknown':
                        pass
                    else:
                        port_info_list = []
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
                            port_info_list.append(
                                result['tcp'][port]['reason'])
                        except:
                            port_info_list.append('None')
                        try:
                            port_info_list.append(
                                result['tcp'][port]['extrainfo'])
                        except:
                            port_info_list.append('None')
                        try:
                            port_info_list.append(result['tcp'][port]['name'])
                        except:
                            port_info_list.append('None')
                        try:
                            port_info_list.append(
                                result['tcp'][port]['version'])
                        except:
                            port_info_list.append('None')
                        port_info_table.add_row(port_info_list)
                        port_info_list = []
                # print(port_info_list)
                print(port_info_table)
                port_info_table = PrettyTable(['IP地址', 'MAC地址', '端口号', '状态', '原因', '额外信息', '名字', '版本'])
            except:
                pass
    print_info('扫描用时' + color.green(str(round(end_time - start_time, 2))) + '秒')
