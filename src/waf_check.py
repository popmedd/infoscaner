from src.color_print import *
import subprocess

def waf_check(url, output=None):
    print_info('使用wafw00f进行waf检测')
    command_str = 'wafw00f -v -a ' + url
    if output == None:
        print_info(command_str)
        command = command_str.split(' ')
        rsp = subprocess.Popen(command)
        rsp.communicate()
    else:
        command = command_str.split(' ')
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait()
        out = p.stdout.read().decode()
        try:
            with open(output, 'w') as fp:
                fp.write(out)
            print_info('wafw00f成功获取WAF信息')
            print_info('保存路径为 ' + color.yellow(output))
        except:
            print_error('输入的文件名错误')