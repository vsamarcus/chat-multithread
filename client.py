import socket
import select
import sys
import threading

if len(sys.argv) < 2:
    print("usage: client SERVER_IP [PORT]")
    sys.exit(1)

ip_address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))

username = input("Informe seu nome de usuário: ")
server.send(username.encode("utf-8"))

def user_input_thread(server_socket):
    while True:
        message = input()
        server_socket.send(message.encode("utf-8"))

# Inicie a thread de entrada do usuário
user_input_thread = threading.Thread(target=user_input_thread, args=(server,))
user_input_thread.daemon = True
user_input_thread.start()

running = True
while running:
    socket_list = [server]
    
    rs, ws, es = select.select(socket_list, [], [])
    if es:
        print("ERR:", es)
    if ws:
        print("WRT:", ws)
    for sock in rs:
        if sock == server:
            message = sock.recv(2048).decode("utf-8")
            if message == "@SAIR":
                print("Você será desconectado.")
                running = False
            else:
                print(message)

server.close()
