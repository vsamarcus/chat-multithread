import socket
import select
import sys

if len(sys.argv) < 2:
    print("usage: client SERVER_IP [PORT]")
    sys.exit(1)

ip_address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))

username = input("Informe seu nome de usuário: ")
server.send(username.encode("utf-8"))

running = True
while running:
    socket_list = [sys.stdin, server]
    
    rs, ws, es = select.select(socket_list, [], [])
    if es:
        print("ERR:", es)
    if ws:
        print("WRT:", ws)
    for sock in rs:
        if sock == server:
            message = sock.recv(2048).decode("utf-8")
            if message == "@SAIR":  # Verifica se o servidor enviou o comando de logout
                print("Você será desconectada.")
                running = False  # Encerra o loop e sai do cliente
            else:
                print(message)
        else:
            message = sys.stdin.readline().strip()
            if message:
                server.send(f"{message}".encode("utf-8"))

server.close()
