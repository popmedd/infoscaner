import paramiko
import re

def ssh_connect(connection_option):
	try:
		if len(connection_option) < 2:
			pass
		elif len(connection_option) == 2:
			ip = connection_option[0]
			user = 'root'
			passwd = connection_option[1]
			cmd = 'uname -a'
			port = 22
		elif len(connection_option) == 3:
			ip = connection_option[0]
			user = connection_option[1]
			passwd = connection_option[2]
			cmd = 'uname -a'
			port = 22
		elif len(connection_option) == 4:
			ip = connection_option[0]
			user = connection_option[1]
			passwd = connection_option[2]
			cmd = connection_option[3]
			port = 22
		elif len(connection_option) == 5:
			ip = connection_option[0]
			user = connection_option[1]
			passwd = connection_option[2]
			cmd = connection_option[3]
			port = connection_option[4]
		else:
			pass

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip, port, user, passwd, timeout = 5)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		exec_cmd_result = stdout.read().decode()
		ssh.close()
		return (1, passwd, exec_cmd_result)

	except Exception as e:
		if re.search('Authentication failed.', str(e)):
			return (0, passwd)
		else:
			pass
		ssh.close()

if __name__ == '__main__':
	result = ssh_connect(['192.168.2.245', 'root', 'root', 'uname -a', 22])
	print(result)