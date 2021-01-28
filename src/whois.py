from src.color_print import *
import requests
import re
from prettytable import PrettyTable
from src.get_user_agent import *
import whois
import nmap
import sys

def chinaz_whois_search(whois_url, write=False, output=None):
    # print(whois_url)
    url = 'http://whois.aizhan.com/'
    result_url = url + whois_url + '/'
    response = requests.get(result_url, headers=get_user_agent()).text
    define_name_re = r'<td class="thead">(.*?)</td>'
    tmp_define_name = re.findall(define_name_re, response)
    define_name = tmp_define_name[:-11]
    result_name_re = r'<td>(.*?)</td>'
    result_name = re.findall(result_name_re, response)
    result = result_name[:-11]
    # print(result)
    if write == False:
        chinaz_whois_table = PrettyTable(['information', 'result'])
        for i in range(len(define_name)):
            tmp_list = []
            tmp_list.append(define_name[i])
            tmp_result = result[i].replace('<span>', '')
            result_prettytable = tmp_result.replace('</span>', '')
            if re.match('<img src="https:', result_prettytable):
                result_prettytable = '-'
            if '<a href' in result_prettytable:
                place = result_prettytable.find('<a href="')
                result_prettytable = result_prettytable[:place]
            tmp_list.append(result_prettytable)
            chinaz_whois_table.add_row(tmp_list)
        print_info('从www.aizhan.com获取whois信息成功 输出whois信息表')
        time.sleep(0.5)
        print(chinaz_whois_table)
    else:
        f = open(output, 'w')
        f.write('www.aizhan.com查询到的信息如下' + '\n\n')
        for i in range(len(define_name)):
            f.write(define_name[i])
            tmp_result = result[i].replace('<span>', '')
            result_prettytable = tmp_result.replace('</span>', '')
            if re.match('<img src="https:', result_prettytable):
                result_prettytable = '-'
            if '<a href' in result_prettytable:
                place = result_prettytable.find('<a href="')
                result_prettytable = result_prettytable[:place]
            f.write('   ' + result_prettytable + '\n')
        print_info('www.aizhan.com成功获取到whois信息')
        print_info('成功将文件写入到' + color.yellow(output))
        # print_info('[target: ' + whois_url + ']' + ' ' + '写入路径为' + color.green(sys.path[0]) + color.green('\\output\\' + whois_url + '_whois.txt'))
        f.close()


def who_is_whois_search(whois_url, write=False, output=None):
    url = 'http://who.is/whois/' + whois_url
    response = requests.get(url, headers=get_user_agent()).text
    block_title = r'<span class="lead">(.*?)</span>'
    registrar_info = re.findall(block_title, response, re.S)[0]
    registrar_who_is_table = PrettyTable([registrar_info, 'Regist Info'])
    tmp_title = r'<div class="col-md-4 queryResponseBodyKey">(.*?)</div>'
    TMP_NAME = re.findall(tmp_title, response, re.S)[0]
    TMP_WHOIS_SERVER = re.findall(tmp_title, response, re.S)[1]
    TMP_REFERRAL_URL = re.findall(tmp_title, response, re.S)[2]
    TMP_STATUS = re.findall(tmp_title, response, re.S)[3]
    NAME = TMP_NAME.replace('Name', '姓名')
    WHOIS_SERVER = TMP_WHOIS_SERVER.replace('Whois Server', 'whois服务器')
    REFERRAL_URL = TMP_REFERRAL_URL.replace('Referral URL', '转介网站')
    STATUS = TMP_STATUS.replace('Status', '状态')
    registrar_info_result_re = r'<div class="col-md-8 queryResponseBodyValue">(.*?)</div>'
    name = re.findall(registrar_info_result_re, response, re.S)[0]
    whois_server = re.findall(registrar_info_result_re, response, re.S)[1]
    referral_url = re.findall(registrar_info_result_re, response, re.S)[2]
    status_re = r'''<div class="col-md-8 queryResponseBodyValue">
(.*?)	    </div>'''
    tmp_status = re.findall(status_re, response, re.S)[0]
    status = tmp_status.replace('<br>', '\n')
    registrar_who_is_table.add_row([NAME, name])
    registrar_who_is_table.add_row([WHOIS_SERVER, whois_server])
    registrar_who_is_table.add_row([REFERRAL_URL, referral_url])
    registrar_who_is_table.add_row([STATUS, status])
    date_whois_table = PrettyTable(['Important Dates', 'DateTime'])
    TMP_EXPIRES_ON = re.findall(tmp_title, response, re.S)[4]
    TMP_REGISTERED_ON = re.findall(tmp_title, response, re.S)[5]
    TMP_UPDATED_ON = re.findall(tmp_title, response, re.S)[6]
    EXPIRES_ON = TMP_EXPIRES_ON.replace('Expires On', '到期时间')
    REGISTERED_ON = TMP_REGISTERED_ON.replace('Registered On', '注册时间')
    UPDATED_ON = TMP_UPDATED_ON.replace('Updated On', '更新时间')
    expires_on = re.findall(registrar_info_result_re, response, re.S)[4]
    registered_on = re.findall(registrar_info_result_re, response, re.S)[5]
    updated_on = re.findall(registrar_info_result_re, response, re.S)[6]
    date_whois_table.add_row([EXPIRES_ON, expires_on])
    date_whois_table.add_row([REGISTERED_ON, registered_on])
    date_whois_table.add_row([UPDATED_ON, updated_on])
    name_server_table = PrettyTable(['Name Server', 'Server IP'])
    name_server_re = r'<a href="/nameserver/(.*?)">(.*?)</a>'
    name_server = re.findall(name_server_re, response)
    name_server_ip_re = r'<a href="/whois-ip/ip-address/(.*?)">(.*?)</a>'
    name_server_ip = re.findall(name_server_ip_re, response)
    for i in range(len(name_server)):
        name_server_table.add_row([name_server[i][1], name_server_ip[i][1]])
    if write == False:
        # print_info('注册信息表')
        print_info('从who.is获取whois信息成功 输出whois注册信息表')
        time.sleep(0.5)
        print(registrar_who_is_table)
        # print_info('时间信息表')
        print_info('从who.is获取whois信息成功 输出whois时间信息表')
        time.sleep(0.5)
        print(date_whois_table)
        print_info('从who.is获取whois信息成功 输出whois Name Servers表')
        time.sleep(0.5)
        print(name_server_table)
    elif write == True:
        f = open(output, 'a')
        f.write('\n\nwho.is查询到的信息如下' + '\n\n')
        f.write(NAME + '      ' + name + '\n')
        f.write(WHOIS_SERVER + '      ' + whois_server + '\n')
        f.write(REFERRAL_URL + '      ' + referral_url + '\n')
        f.write(STATUS + '      ' + status + '\n')
        f.write('\n')
        f.write(EXPIRES_ON + '      ' + expires_on + '\n')
        f.write(REGISTERED_ON + '      ' + registered_on + '\n')
        f.write(UPDATED_ON + '      ' + updated_on + '\n')
        f.write('\n')
        for i in range(len(name_server)):
            f.write(name_server[i][1] + '      ' + name_server_ip[i][1] + '\n')
        print_info('who.is成功获取到whois信息')
        print_info('成功将文件写入到' + color.yellow(output))
    else:
        print_error('参数错误')
    

def python_whois_search(url, output=None):
    print_info('通过python模块获取whois信息')
    whois_info = {}
    try:
        whois_info = whois.whois(url)
    except:
        print_error('输入的url格式有问题')
        print_error('退出程序')
        exit(0)
    if output == None:
        for k, v in whois_info.items():
            print(color.blue('------------------' + str(k) + '--------------------'))
            print(color.yellow(str(k) + '  ' + str(v)))
            print(color.blue('---------------------------------------------\n'))
    else:
        try:
            f = open(output, 'a')
            f.write('\n\n----------------------------python-whois----------------------------\n')
            for k, v in whois_info.items():
                f.write('------------------' + str(k) + '--------------------' + '\n')
                f.write(str(k) + '  ' + str(v) + '\n')
                f.write('---------------------------------------------\n')
            f.close()
            print_info('who.is成功获取到whois信息')
            print_info('成功将文件写入到' + color.yellow(output))
        except:
            print_error('输出路径错误')