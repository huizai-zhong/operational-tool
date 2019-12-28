'''
并行批量管理远程服务器

Usage: python remote_comm.py 服务器IP地址文件 "需要执行的命令"
Example: python remote_comm.py serverips.txt "useradd dcc"
'''

import sys
import os
import getpass
import threading
import paramiko

def remote_comm(host, passwd, command):
    # 创建用于连接SSH服务器的实例
    ssh = paramiko.SSHClient()
    # 设置自动添加主机秘钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    # 连接ssh服务器，输入连接的主机，用户名，密码
    ssh.connect(hostname=host, username='root', password=passwd)
    # 在ssh服务器上执行指定命令，返回3项类文件对象，分别是，输入、输出、错误
    stdin, stdout, stderr = ssh.exec_command(command)
    # 读取输出
    out = stdout.read()
    # 读取错误
    error = stderr.read()
    # 如果有输出和错误则打印出来
    if out:
        print('[%s] OUT : \n %s' % (host, out.decode('utf8')))
    if error:
        print('[%s] ERROR : \n %s' % (host, error.decode('utf8')))
    # 程序结束
    ssh.close()
    


if __name__ == "__main__":
    # 设定sys.argv长度，确保remote_comm.py函数中的参数数量
    if len(sys.argv) != 3:
        print(f'Usage: python {sys.argv[0]} ipaddr_file "command"')
        exit(1)
    # 判断服务器IP地址文件是否存在
    if not os.path.isfile(sys.argv[1]):
        print('No such file:', sys.argv[1])
        exit(2)
    
    ipaddr_file = sys.argv[1]
    command = sys.argv[2]
    # 通过getpass获取服务器密码
    passwd = getpass.getpass()
    # 打开ipaddr_file，将文件中ip地址提取出来以列表的形式存储起来
    with open(ipaddr_file) as fobj:
        # line.strip() 可去掉每行ip后的\n
        ips = [line.strip() for line in fobj ]

    for ip in ips:
        # 创建多线程实例
        t = threading.Thread(target=remote_comm, args=(ip, passwd, command))
        # 启动
        t.start()

