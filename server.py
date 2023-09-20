import socket
import sys
import threading

client_usernames = {}

def chat_client(conn, addr):
    client_connected = True
    try:
        username = conn.recv(2048).decode("utf-8")
        if not username:
            conn.send("O nome de usuário não pode ficar vazio.".encode("utf-8"))
            client_connected = False
        elif username in client_usernames.values():
            conn.send("O nome de usuário já está em uso.".encode("utf-8"))
            client_connected = False
        else:
            client_usernames[conn] = username

        while client_connected:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message == "@SAIR":  # Verifica se o cliente enviou o comando de logout
                    conn.send("@LOGOUT".encode("utf-8"))  # Envia um comando de logout de volta ao cliente
                    del client_usernames[conn]
                    conn.close()
                    client_connected = False
                else:
                    formatted_message = f"{username}:: {message}"
                    print(formatted_message)
                    for client_conn in client_usernames.keys():
                        if client_conn != conn:
                            client_conn.send(formatted_message.encode("utf-8"))
            else:
                client_connected = False
    except Exception as ex:
        print("ERROR: ", ex)
    finally:
        del client_usernames[conn]
        conn.close()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('0.0.0.0', port))

server.listen(5)

running = True
while running:
    conn, addr = server.accept()
    client_thread = threading.Thread(target=chat_client, args=(conn, addr))
    client_thread.start()

server.close()