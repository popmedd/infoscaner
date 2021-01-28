from src.color_print import *
from prettytable import PrettyTable
import nmap

def nmap_http_head(url):
    print_info('对' + color.green(url) + '进行HTTP头部信息获取')
    nm = nmap.PortScanner()
    scan_raw_result = nm.scan(
        hosts=url, arguments='-p 80 --script=http-headers')
    for host, result in scan_raw_result['scan'].items():
        if result['status']['state'] == 'up':
            head = result['tcp'][80]['script']['http-headers'].replace('  ', '|  ')
            print(head)
        else:
            print_error(url + color.red('未存活'))