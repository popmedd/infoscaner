from src.color_print import *
import requests
import re
from prettytable import PrettyTable
import sys
from src.get_user_agent import *


def icp_search(ICP, write=False, output=None):
    print_info('从icp.aizhan.com查询ICP备案号')
    url = 'https://icp.aizhan.com/'
    result_url = url + ICP + '/'
    info_table = PrettyTable(['Searching', 'Result'])
    response = requests.get(result_url, headers=get_user_agent()).text
    info_re = r'<td>(.*?)</td>'
    
    sponsor_name = re.findall(info_re, response, re.S)[0]
    info_table.add_row(['主办单位名称', sponsor_name])

    sponsor_quality = re.findall(info_re, response, re.S)[1]
    info_table.add_row(['主办单位性质', sponsor_quality])

    sponsor_quality = re.findall(info_re, response, re.S)[2]
    tmp_sponsor_quality = sponsor_quality.replace('<span>', '')
    sponsor_quality = tmp_sponsor_quality.replace('</span>', '')
    info_table.add_row(['备案号', sponsor_quality])

    website_name = re.findall(info_re, response, re.S)[3]
    # print(website_name)
    info_table.add_row(['网站名称', website_name])

    tmp_website_home = re.findall(info_re, response, re.S)[4]
    website_home = tmp_website_home.replace('<br />', '\n')
    # print(website_home)
    info_table.add_row(['网站首页地址', website_home])

    tmp_authentication = re.findall(info_re, response, re.S)[5]
    authentication_re = r'<a href="(.*?)" ref="nofollow" target="_blank">'
    authentication = re.findall(authentication_re, tmp_authentication, re.S)[0]
    info_table.add_row(['认证', authentication])
    # print(authentication)

    website_domain_name = re.findall(info_re, response, re.S)[6]
    info_table.add_row(['网站域名', website_domain_name])
    # print(website_domain_name)

    audit_time = re.findall(info_re, response, re.S)[7]
    tmp_time = audit_time.replace('<span>', '')
    audit_time = tmp_time.replace('</span>', '')
    info_table.add_row(['审核时间', audit_time])

    icp_table = PrettyTable(['该单位备案网站', '网站名称', '网站首页地址', '审核时间'])
    website_icp_list_re = r'<td class="center"><span>(.*?)</span></td>'
    website_icp_list = re.findall(website_icp_list_re, response)
    # print(website_icp_list[:-2])
    website_name_two_re = r'<td class="center">(.*?)</td>'
    website_name_two = re.findall(website_name_two_re, response)[5:-2:2]
    # print(re.findall(website_name_two_re, response))
    # print(website_icp_list)
    website_home_url_re = r'''<td class="center"><span class="blue">
																									(.*?)																						</span></td>
										<td class="center">'''
    website_home_url = re.findall(website_home_url_re, response)

    website_audit_time_re = r'''<td class="center">
											<span>
																									(.*?)																							</span>
										</td>'''
    website_audit_time = re.findall(website_audit_time_re, response)
    # print(website_audit_time)
    # print(website_home_url)
    if write == False:
        print(info_table)
        for i in range(0, len(website_icp_list) - 2):
            website_name_two_list = []
            website_name_two_list.append(website_icp_list[i])
            website_name_two_list.append(website_name_two[i])
            website_name_two_list.append(website_home_url[i].replace('<br />', '\n'))
            website_name_two_list.append(website_audit_time[i])
            icp_table.add_row(website_name_two_list)
        print_info('成功获取ICP信息')
        print(icp_table)
    elif write == True:
        f = open(output, 'w')
        print_info('成功获取ICP信息')
        print_info('保存路径为' + color.yellow(output))
        f.write('主办单位名称       ' + sponsor_name + '\n')
        f.write('主办单位性质       ' + sponsor_quality + '\n')
        f.write('网站名称       ' + website_name + '\n')
        f.write('网站首页地址       ' + website_home + '\n')
        f.write('认证       ' + authentication + '\n')
        f.write('网站域名       ' + website_domain_name + '\n')
        f.write('备案号         ' + sponsor_quality + '\n')
        f.write('审核时间       ' + audit_time + '\n')
        f.write('该单位备案网站                 网站名称                网站首页地址                审核时间\n\n\n')
        for i in range(0, len(website_icp_list) - 2):
            f.write(website_icp_list[i] + '             ' + website_name_two[i] +
                    '         ' + website_home_url[i] + '        ' + website_audit_time[i] + '\n')
        f.close()
    else:
        print_error('参数错误')


def chinaz_icp_search(target_url, output=None):
    print_info('从icp.chinaz.com获取ICP备案信息')
    url = 'http://icp.chinaz.com/'
    info_table = PrettyTable(['Searching', 'Result'])
    if output != None:
        f = open(output, 'a')
        f.write('\n\nicp.chinaz.com\n\n')
    result_url = url + target_url
    # print(result_url)
    response = requests.get(result_url, headers=get_user_agent()).text
    try:
        sponsor_name_re = r'<a target="_blank" href="(.*?)">(.*?)</a>'
        sponsor_name = re.findall(sponsor_name_re, response)[0][1]
        info_table.add_row(['主办单位名称', sponsor_name])
        f.write('主办单位名称   ' + sponsor_name + '\n')
    except:
        pass
    try:
        sponsor_quality_re = r'<p><strong class="fl fwnone">(.*?)</strong></p>'
        sponsor_quality = re.findall(sponsor_quality_re, response)[0]
        info_table.add_row(['主办单位性质', sponsor_quality])
        f.write('主办单位性质   ' + sponsor_quality + '\n')
    except:
        pass
    try:
        ICP = re.findall('<p><font>(.*?)</font>', response)[0]
        info_table.add_row(['网站备案/许可证号', ICP])
        f.write('网站备案/许可证号  ' + ICP + '\n')
    except:
        pass
    try:
        website_name = re.findall('<p>(.*?)</p>', response)[2]
        info_table.add_row(['网站名称', website_name])
        f.write('网站名称   ' + website_name + '\n')
    except:
        pass
    try:
        website_home_url = re.findall('<p class="Wzno">(.*?)</p>', response)[0]
        info_table.add_row(['网站首页地址', website_home_url])
        f.write('网站首页地址   ' + website_home_url + '\n')
    except:
        pass
    try:
        time_re = r'<p>(.*?)</p>'
        time = re.findall(time_re, response)[-1]
        # print(time)
        info_table.add_row(['审核时间', time])
        f.write('审核时间   ' + time + '\n')
    except:
        pass
    print(info_table)
    if output != None:
        print_info('从chinaz获取ICP信息并保存到' + color.yellow(output))
        f.close()