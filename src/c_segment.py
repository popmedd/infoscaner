from src.color_print import *
import requests
import re
from prettytable import PrettyTable
import sys
from src.get_user_agent import *

def c_segment_search(c_segment_url, write=False, output=None):
    ip_list = PrettyTable(['Searching', 'Result'])
    print_info('查询旁站和C段')
    url = 'http://webscan.cc/site_'
    result_url = url + c_segment_url + '/'
    # print(result_url)
    response = requests.get(result_url, headers=get_user_agent(), verify=False).text
    domain_ip_re = r'<h1>(.*?)</h1>'
    domain_ip = re.findall(domain_ip_re, response, re.S)[0]
    company_re = r'<h2>(.*?)</h2>'
    company = re.findall(company_re, response, re.S)[0]
    container_re = r'<td><p>(.*?)</p></td>'
    container = re.findall(container_re, response, re.S)[1]
    if write == False:
        ip_list.add_row(['IP地址', domain_ip])
        ip_list.add_row(['公司', company])
        ip_list.add_row(['站点容器', container])
        title_re = r'<li class="J_link"><span>(.*?)</span>'
        title = re.findall(title_re, response)
        domain_result_re = r'target="_blank">(.*?)</a></li>'
        domain_result = re.findall(domain_result_re, response)
        # print(title)
        # print(domain_result)
        print_info('输出站点信息表')
        time.sleep(0.5)
        print(ip_list)
        same_table = PrettyTable(['title', 'url'])
        for i in range(len(title)):
            list_domain = []
            list_domain.append(title[i])
            list_domain.append(domain_result[i])
            # print(list_domain)
            same_table.add_row(list_domain)
        print_info('同服IP站点列表')
        time.sleep(0.5)
        print(same_table)
    else:
        f = open(output, 'w')
        f.write(c_segment_url + '\n\n')
        f.write('IP地址  ' + domain_ip + '\n')
        f.write('公司  ' + company + '\n')
        f.write('站点容器  ' + container + '\n\n\n')
        title_re = r'<li class="J_link"><span>(.*?)</span>'
        title = re.findall(title_re, response)
        domain_result_re = r'target="_blank">(.*?)</a></li>'
        domain_result = re.findall(domain_result_re, response)
        for i in range(len(title)):
            f.write(title[i] + '  ' + domain_result[i] + '\n')
        print_info('成功获取C段和旁站信息')
        print_info('保存路径为 ' + color.yellow(output))
        f.close()
