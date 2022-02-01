#!/usr/bin/python3
#9th of January 2022
#Use paramiko to SSH into remote machines and run commands, then output them into a file.

import paramiko

ip = 'x.x.x.x'
file = open('ips.txt', 'r')
ip = file.read().splitlines()

for i in ip:
    try:
        out = open('output.txt', 'a')
        out.write(i+'\n')
        client = paramiko.SSHClient()
        client.load_host_keys('/home/xzivye/.ssh/known_hosts')
        client.load_system_host_keys()
        key = paramiko.RSAKey.from_private_key_file('/home/xzivye/.ssh/id_rsa', password=None)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(i, pkey=key)

        stdin, stdout, stderr = client.exec_command('cat /etc/hostname')
        out.write(f'Hostname: {stdout.read().decode("utf8")}')
        stdin.close()
        stdout.close()
        stderr.close()

        stdin, stdout, stderr = client.exec_command('ls -a /var/www')
        if stdout != []:
            out.write('There are files in the www directory.\n\n')
        else:
            out.write('There are no files in the www directory.\n\n')
        stdin.close()
        stdout.close()
        stderr.close()
        out.close()
        client.close()

    except paramiko.client.NoValidConnectionsError:
        print(i,' is offline')
        out.write('Machine was offline. No data could be obtained.\n\n')
file.close()