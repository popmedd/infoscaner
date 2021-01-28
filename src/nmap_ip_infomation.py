from src.color_print import *
from prettytable import PrettyTable
import nmap

def nmap_ip_infomation(url):
    port_info_table = PrettyTable(
        ['IP地址', 'MAC地址', '端口号', '状态', '原因', '额外信息', '名字', '版本'])
    print_info('对' + color.green(url) + '进行IP信息查询')
    nm = nmap.PortScanner()
    scan_raw_result = nm.scan(hosts=url, arguments='--script  ip-geolocation-*')
    for host, result in scan_raw_result['scan'].items():
        if result['status']['state'] == 'up':
            hostnames_table = PrettyTable(['查询', '结果'])
            # print(result['hostnames'])
            for i in result['hostnames']:
                for key,value in i.items():
                    try:
                        hostnames_table.add_row([key, value])
                    except:
                        pass
            print(hostnames_table)
            try:
                for port in result['tcp']:
                    try:
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
                    except:
                        pass
                print(port_info_table)
            except:
                pass
            hostnames_script_table = PrettyTable(['查询', '结果'])
            # print(result['hostscript'])
            for script in result['hostscript']:
                for key, value in script.items():
                    try:
                        tmp_value = value.replace('\n', '')
                        value = tmp_value
                        hostnames_script_table.add_row([key, value])
                    except:
                        pass
            print(hostnames_script_table)
        else:
            print_error(url + color.red('未存活'))
