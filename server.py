import sockets
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

