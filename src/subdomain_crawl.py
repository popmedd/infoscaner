from src.color_print import *
import requests
import re
from prettytable import PrettyTable
import sys
from src.get_user_agent import *

def subdomain_crawl(subdomain_url, write=False):
    url = 'http://tool.chinaz.com/subdomain/?domain='
    result_url = url + subdomain_url
    # print(result_url)
    response = requests.post(result_url, headers=get_user_agent()).text
    # print(response)
    re_page = r'</a><span class="col-gray02">共(.*?)页，到第</span>'
    page = int(re.findall(re_page, response, re.S)[0])
    if write == False:
        print_info('查询' + color.green(subdomain_url) + '的子域名')
        subdomain_table = PrettyTable(['子域名'])
        if page == 1:
            temp_re_subdomain = r'<div class="w23-0 subdomain">(.*?)</a></div>'
            temp_subdomain = re.findall(temp_re_subdomain, response)
            list_subdomain = []
            for i in temp_subdomain:
                re_subdomain = r'domain=(.*?)" target="_blank">'
                subdomain = re.findall(re_subdomain, i, re.S)
                list_subdomain.append(subdomain)
                subdomain_table.add(subdomain)
        else:
            for i in range(1, page):
                subdomain_page_url = 'http://tool.chinaz.com/subdomain?domain=' + subdomain_url + '&page=' + \
                    str(i)
                response = requests.post(
                    subdomain_page_url, headers=get_user_agent()).text
                temp_re_subdomain = r'<div class="w23-0 subdomain">(.*?)</a></div>'
                temp_subdomain = re.findall(temp_re_subdomain, response)
                # print(temp_subdomain)
                list_subdomain = []
                for i in temp_subdomain:
                    re_subdomain = r'domain=(.*?)" target="_blank">'
                    subdomain = re.findall(re_subdomain, i, re.S)
                    # subdomain_table.add(subdomain)
                    subdomain_table.add_row(subdomain)
        print(subdomain_table)
    else:
        f = open('./output/' + subdomain_url + '_subdomain.txt', 'w')
        if page == 1:
            temp_re_subdomain = r'<div class="w23-0 subdomain">(.*?)</a></div>'
            temp_subdomain = re.findall(temp_re_subdomain, response)
            list_subdomain = []
            for i in temp_subdomain:
                re_subdomain = r'domain=(.*?)" target="_blank">'
                subdomain = re.findall(re_subdomain, i, re.S)
                list_subdomain.append(subdomain)
                subdomain_table.add(subdomain)
        else:
            for i in range(1, page):
                subdomain_page_url = 'http://tool.chinaz.com/subdomain?domain=' + subdomain_url + '&page=' + \
                    str(i)
                response = requests.post(
                    subdomain_page_url, headers=get_user_agent()).text
                temp_re_subdomain = r'<div class="w23-0 subdomain">(.*?)</a></div>'
                temp_subdomain = re.findall(temp_re_subdomain, response)
                # print(temp_subdomain)
                list_subdomain = []
                for i in temp_subdomain:
                    re_subdomain = r'domain=(.*?)" target="_blank">'
                    subdomain = re.findall(re_subdomain, i, re.S)[0]
                    f.write(subdomain + '\n')
            print_info('写入完成')
            print_info('写入路径为' + color.green(sys.path[0]) + color.green(
                '\\output\\' + subdomain_url + '_subdomain.txt'))
            f.close()
