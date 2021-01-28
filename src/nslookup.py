from src.color_print import *
import requests
import re
from prettytable import PrettyTable
import sys
import subprocess
import time


def run_command(command_str):
    command = command_str.split(' ')
    rsp = subprocess.Popen(command)
    rsp.communicate()


def get_command_output(command_str):
    command = command_str.split(' ')
    rsp = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = rsp.stdout.read().decode('gbk')
    return output


def nslookup_search(url, write=False, output=None):                       # nslookup查询
    if output == None:
        print_info('Nslookup Scan ' + url)
        nslookup_A_command_str = 'nslookup ' + url
        print_info('Searching A address record(IPv4)')
        try:
            run_command(nslookup_A_command_str)
        except:
            pass
        nslookup_AAAA_command_str = 'nslookup -qt=AAAA ' + url
        print_info('Searching AAAA address record(IPv6)')
        try:
            run_command(nslookup_AAAA_command_str)
        except:
            pass
        nslookup_AFSDB_command_str = 'nslookup -qt=ns ' + url
        print_info('View the naming server NS')
        try:
            run_command(nslookup_AFSDB_command_str)
        except:
            pass
        nslookup_CNAME_command_str = 'nslookup -d3 ' + url
        print_info('Check how long DNS cache records have been kept')
        try:
            run_command(nslookup_CNAME_command_str)
        except:
            pass

    else:
        f = open(output, 'w')
        print_info('Nslookup Scan ' + url)
        nslookup_A_command_str = 'nslookup ' + url
        print_info('Searching A address record(IPv4)')
        try:
            a_content = get_command_output(nslookup_A_command_str)
            f.write('Searching A address record(IPv4)\n\n' + a_content)
        except:
            pass
        nslookup_AAAA_command_str = 'nslookup -qt=AAAA ' + url
        print_info('Searching AAAA address record(IPv6)')
        try:
            aaaa_content = get_command_output(nslookup_AAAA_command_str)
            f.write('Searching AAAA address record(IPv6)\n\n' + aaaa_content)
        except:
            pass
        nslookup_NS_command_str = 'nslookup -qt=ns ' + url
        print_info('View the naming server NS')
        try:
            ns_content = get_command_output(nslookup_NS_command_str)
            f.write('View the naming server NS\n\n' + ns_content)
        except:
            pass
        nslookup_d3_command_str = 'nslookup -d3 ' + url
        print_info('Check how long DNS cache records have been kept')
        try:
            d3_content = get_command_output(nslookup_d3_command_str)
            f.write('Check how long DNS cache records have been kept\n\n' + d3_content + '\n')
        except:
            pass
        f.close()
        print_info('获取信息成功')
        print_info('文件保存到' + color.yellow(output))
