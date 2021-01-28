from src.color_print import *
from prettytable import PrettyTable
import nmap
import sys

def nmap_dns_brute(url, write=False):
    if write == False:
        dns_table = PrettyTable(['域名', 'IP'])
        print_info('对' + color.green(url) + '进行DNS信息收集')
        print_info('大约需要' + color.green('3-7') + '分钟')
        nm = nmap.PortScanner()
        scan_raw_result = nm.scan(
            hosts=url, arguments='--script dns-brute')
        for host, result in scan_raw_result['scan'].items():
            if result['status']['state'] == 'up':
                for hostscript in result['hostscript']:
                    tmp_dns = hostscript['output'].split('\n')
                    for i in range(2, len(tmp_dns)):
                        result = tmp_dns[i].replace(' ', '')
                        tmp_result_list = result.split('-')
                        dns_table.add_row([tmp_result_list[0], tmp_result_list[1]])
                print(dns_table)
            else:
                print_error(url + color.red('未存活'))
    elif write == True:
        dns_list = []
        nm = nmap.PortScanner()
        scan_raw_result = nm.scan(hosts=url, arguments='--script dns-brute')
        for host, result in scan_raw_result['scan'].items():
            if result['status']['state'] == 'up':
                for hostscript in result['hostscript']:
                    tmp_dns = hostscript['output'].split('\n')
                    for i in range(2, len(tmp_dns)):
                        result = tmp_dns[i].replace(' ', '')
                        tmp_result_list = result.split('-')
                        dns_list.append([tmp_result_list[0], tmp_result_list[1]])
        f = open('./output/' + url + '_dns_info.txt', 'w')
        for domain, ip in dns_list:
            f.write(domain + '      ' + ip + '\n')
        print_info('写入完成')
        print_info('写入路径为' + color.green(sys.path[0]) + color.green('\\output\\' + url + '_dns_info.txt'))
        f.close()
    else:
        print_error('参数错误')
