import socket
import select
import sys
from _thread import *

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

if len(sys.argv)!=3:
    print("Correct ussage:,script,IP addres,port number")
    exit()
IP_address=str(sys.argv[1])
Port=int(sys.argv[2])

server.bind((IP_address,Port))

server.listen(100)

list_of_clients=[]
def clientthread(conn,addr):
    conn.send("Welcome to Chatroom".encode())
    while True:
        try:
            message=conn.recv(2048)
            if message:
                print("<"+addr[0]+">"+message.decode())
                message_to_send="<"+addr[0]+">"+message.decode()
                broadcast(message_to_send.encode(),conn)
            else:
                remove(conn)
        except:
            continue
def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
while True:
    conn,addr=server.accept()
    list_of_clients.append(conn)
    print(addr[0]+" Connected")
    start_new_thread(clientthread,(conn,addr))
conn.close()
server.close()
#python3 server.py 192.168.43.221 8080
#cd /mnt/c/users/harsh/desktop/projects/chatbox