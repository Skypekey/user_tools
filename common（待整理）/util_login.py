#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import requests
import paramiko
import telnetlib
import ftplib
import base64
import urllib3
import time


def ssh(ip, port, user, pwd, cmd=None, timeout=5, encoding="UTF-8"):
    """尝试进行 ssh 登录。登录成功返回 True，登录异常返回异常信息。\n
    若 cmd 不为空，则登录后执行 cmd 命令。返回 cmd 命令执行结果。

    params ip(str): 登录主机的 IP 地址。
    params port(str): 登录主机的 SSH 端口。
    params user(str): 登录主机的用户。
    params pwd(str): 登录主机的登录用户所属的密码。
    params cmd(str): 登录主机后执行的命令。默认不执行命令。
    params timeout(str): 登录主机时的超时时间。默认 5 秒。
    params encoding(str): 登录主机后所执行命令返回结果的解码方式。默认 UTF-8。

    return tuple(int, bool|str):
        返回 (0, True): 代表登录成功。
        返回 (1, str): 代表命令执行成功及执行结果。
        返回 (2, str(e)): 代表登录异常及异常信息。"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, pwd, timeout=timeout)
        if cmd:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            ssh_result = stdout.read().decode(encoding)
            return 1, ssh_result
        else:
            return 0, True
    except Exception as e:
        return 2, str(e)


def telnet(ip, port, user, pwd):
    try:
        tn = telnetlib.Telnet(ip, timeout=5)
        tn.set_debuglevel(0)
        tn.read_until("login: ")
        tn.write(user + '\r\n')
        tn.read_until("assword: ")
        tn.write(pwd + '\r\n')
        result = tn.read_some()
        result = result+tn.read_some()
        if result.find('Login Fail') > 0 or result.find('incorrect') > 0:
            print("[-] Checking for "+user, pwd+" fail")
        else:
            print("[+] Success login for "+user, pwd)
        tn.close()


def ftp_anonymous(ip, port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port, 2)
        ftp.login()
        ftp.quit()
        print('[+] FTP login for anonymous')
    except Exception as e:
        print('[-] checking for FTP anonymous fail')


def ftp_login(ip, port, user, pwd):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port, 2)
        ftp.login(user, pwd)
        ftp.quit()
        print('[+] FTP weak password: '+user, pwd)
    except Exception as e:
        print('[-] checking for '+user, pwd+' fail')


def phpMyAdmin_login(ip, port, user, pwd):
    try:
        url = "http://"+ip+":"+str(port)+"/phpmyadmin/index.php"
        data = {'pma_username': user, 'pma_password': pwd}
        response = requests.post(url, data=data, timeout=5)
        result = response.content

        if result.find('name="login_form"') == -1:
            print('[+] find phpMyAdmin weak password in：'+url)
            print('[+] find phpMyAdmin weak password：'+user, pwd)
        else:
            print('[-] Checking for '+user, pwd+" fail")
            time.sleep(2)
    except Exception as e:
        print('[-] Something Error'+user, pwd+" fail")


def tomcat_login(ip, port, user, pwd):
    try:
        url = "http://"+ip+":"+str(port)+"/manager/html"
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        Authorization = "Basic %s" % (base64.b64encode(user+':'+pwd))
        header = {'User-Agent': user_agent, 'Authorization': Authorization}
        request = urllib3.Request(url, headers=header)
        response = urllib3.urlopen(request, timeout=5)
        result = response.read()
        if response.code == 200:
            print('[Success] ' + url+' '+user+':'+pwd)
    except Exception as e:
        print('[Login failed]' + url+' '+user+':'+pwd)
