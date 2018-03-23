# -*- coding: utf-8 -*-
import socket
import sys

# creamos el socket (permite conectar 2 computadoras)
def socket_create():
    try:
        global host
        global port
        global s #socket
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error" + str(msg))

# Enlazando el socket al puertto y esperando por conexiones desde el cliente.
def socket_bind():
    try:
        global host
        global port
        global s #socket
        print("Binding socket to port " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error" + str(msg) + "\n" + "Retrying...")
        socket_bind()

# Estableciendo conexión con el cliente  (el socket está esperando por esto)
def socket_accept():
    conn, address = s.accept() #Acepta una nueva conexión
    print("Connection has been establish |" +  "IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    conn.close()

# Enviando comandos
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")

def main():
    socket_create()
    socket_bind()
    socket_accept()


main()

