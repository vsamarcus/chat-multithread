import socket
import sys
import threading
from datetime import datetime

usernames = {}
messages = []

def chat_client(conn, addr):
    client_connected = True
    try:
        username = conn.recv(2048).decode("utf-8")
        if not username:
            conn.send("O nome de usuário não pode ficar vazio.".encode("utf-8"))
            client_connected = False
        elif username in usernames.values():
            conn.send("O nome de usuário já está em uso.".encode("utf-8"))
            client_connected = False
        else:
            usernames[conn] = username

        while client_connected:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message == "@SAIR":
                    conn.send("@SAIR".encode("utf-8"))
                    del usernames[conn]
                    conn.close()
                    client_connected = False
                elif message == "@ORDENAR":
                    send_ordered_messages(conn)
                else:
                    formatted_message = f"{username}:: {message}"
                    store_message(formatted_message)
                    for client_conn in usernames.keys():
                        if client_conn != conn:
                            client_conn.send(formatted_message.encode("utf-8"))
            else:
                client_connected = False
    except Exception as ex:
        print("ERROR: ", ex)
    finally:
        del usernames[conn]
        conn.close()

def store_message(message):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    with threading.Lock():
        messages.append((timestamp, message))
    
    with threading.Lock():
        if len(messages) > 15:
            messages.pop(0)

def send_ordered_messages(conn):
    with threading.Lock():
        ordered_messages = sorted(messages, key=lambda x: x[0])
    
    for timestamp, message in ordered_messages[-15:]:
        formatted_message = f"[{timestamp}] - {message}"
        conn.send(formatted_message.encode("utf-8") + b'\n')

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