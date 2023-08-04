# import socket
# import time
#
#
# IS_ONLINE = False
# CLIENT_CONNECTIONS = []
#
# FORMAT = 'utf-8'
#
#
# def User(conn, addr):
#     dis_msg = ""
#     msg = f"Welcome user {str(addr)}"
#     conn.sendall(msg.encode("utf-8"))
#     CONNECTED = True
#     ADDRESS = addr[0]
#     CLIENT_PORT = addr[1]
#     while CONNECTED:
#         message = conn.recv(1024).decode(FORMAT)
#         if message:
#             pr_msg = f"[{str(ADDRESS)}, {str(CLIENT_PORT)}]:{str(message)}"
#             print(pr_msg)
#
#     dis_msg = f"\nUser {addr} Disconnected....."
#     print("client disconnected....")
#     print(dis_msg)
#
#
# def Server(host, port):
#     addr = (host, port)
#     server_close = False
#
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server.bind(addr)
#
#     print(f"Server listening on: {host}:{port}")
#     server.listen()
#
#     while not server_close:
#         conn, addr = server.accept()
#         CLIENT_CONNECTIONS.append(conn)
#         clientThread = CustomThread(target=User, daemon=True, args=(conn, addr))
#         clientT hread.start()
#
#
# def StartServer(host, port):
#     global serverThread
#     serverThread = CustomThread(target=Server, daemon=True, args=(host, port))
#     serverThread.start()
#
#
# def StopServer():
#     if len(CLIENT_CONNECTIONS) > 0:
#         for conn in CLIENT_CONNECTIONS:
#             conn.close()
#     print("disconnecting all clients if connected! ")
#     serverThread.kill()
#
#
# StartServer("localhost", 65432)
# time.sleep(60)
#
# --------------------------------------both end can send and receive data via single socket
#
# import socket
# import threading
#
#
# def receive_data(sock):
#     while True:
#         data = sock.recv(1024)
#         if not data:
#             break
#
#         print(f"\n\>: {data.decode()}", end="\n")
#
#
# def handle_client(client_socket):
#     receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
#     receive_thread.start()
#     while True:
#         # Send a response back to the client
#         msg = input("Enter a msg: ")
#         client_socket.sendall(msg.encode(encoding="utf-8"))
#         if msg.lower() == "exit":
#             break
#
#     client_socket.close()
#
#
# def run_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(("localhost", 8000))
#     server_socket.listen(1)
#
#     print("Server listening on port 8000...")
#
#     client_socket, client_address = server_socket.accept()
#     print(f"Client connected: {client_address}")
#
#     # Start a separate thread to handle client messages
#     client_thread = threading.Thread(target=handle_client, args=(client_socket,))
#     client_thread.start()
#
#     # Main thread for server input and sending messages to client
#     # while True:
#     #     message = input("Enter a message to send to client: ")
#     #     client_socket.sendall(message.encode())
#     #
#     #     if message.lower() == "exit":
#     #         break
#
#     # Wait for the client thread to complete
#     client_thread.join()
#
#     client_socket.close()
#     server_socket.close()
#
#
# if __name__ == "__main__":
#     run_server()
#
# -------------------------------------------two threads for sending and receiving data
#
# import socket
# import threading
# import queue
# import time
# from threading import Semaphore
# import tkinter as tk
# from tkinter import *
#
#
# SERVER_ONLINE = True
# CLIENT_SOCKET = []
#
#
# def client_receive_data(sock):
#     while True:
#         data = sock.recv(1024)
#         print(data.decode('utf-8'))
#
#
# def handle_client(client_socket):
#     receive_thread = threading.Thread(target=client_receive_data, daemon=True, args=(client_socket,))
#     receive_thread.start()
#     while True:
#         msg = input("Enter a msg: ")
#         client_socket.sendall(msg.encode(encoding="utf-8"))
#         if msg.lower() == "exit":
#             break
#
#     client_socket.close()
#
#
# def run_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(("localhost", 8000))
#     server_socket.listen(1)
#
#     print("Server listening on port 8000...")
#
#     while SERVER_ONLINE:
#         conn, addr = server_socket.accept()
#         print(f"Client connected: {conn}")
#
#         CLIENT_SOCKET.append(conn)
#         client_thread = threading.Thread(target=handle_client, daemon=True, args=(conn,))
#         client_thread.start()
#         # client_thread.join()
#
#     for client_socket in CLIENT_SOCKET:
#         client_socket.close()
#     server_socket.close()
#
#
# if __name__ == "__main__":
#     serverThread = threading.Thread(target=run_server, daemon=True)
#     serverThread.start()
#     time.sleep(20)
#     print(CLIENT_SOCKET)
#     CLIENT_SOCKET[0].sendall("i'm server".encode('utf-8'))
#
#
# ------------------------------------------
#
#
# import socket
# from threading import Thread
# from IPmapping import mapping
#
# FORMAT = 'utf-8'
# CLIENT_THREAD = []
#
#
# def receive_client_msg(sock, addr):
#     while True:
#         data = sock.recv(1024).decode(FORMAT)
#         if data:
#             if mapping.is_exists(ip=addr[0]):
#                 name = mapping.get_name_with_ip(addr[0])
#                 print(f"{name}/: {data}")
#             else:
#                 print(f"NEW CLIENT:[{addr}]/: {data}")
#
#             if data.title() == "/Exit":
#                 sock.close()
#                 print("client disconnected....")
#                 break
#
#
# def handle_client(client_socket, addr):
#     client_receive_thread = Thread(target=receive_client_msg, daemon=True, args=(client_socket, addr))
#     client_receive_thread.start()
#
#
# def start_server(host, port):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind((host, port))
#     server_socket.listen()
#
#     while True:
#         conn, addr = server_socket.accept()
#         client_thread = Thread(target=handle_client, daemon=True, args=(conn, addr))
#         client_thread.start()
#
#         CLIENT_THREAD.append(client_thread)
#
#
# host = "localhost"
# port = 65432
#
# Server = Thread(target=start_server, daemon=True, args=(host, port))
# Server.start()
#
# for client in CLIENT_THREAD:
#     client.join()
#
# Server.join()
#
#
#
#
#
import queue
# ---------------------------------class based of above- final


import socket
import time
from IPmapping import mapping
from CUSTOM_THREAD import thread_with_trace as CThread
import threading
import queue

FORMAT = 'utf-8'


class SocketBindingException(Exception):
    pass


class QueueEmpty(Exception):
    pass


class LockingMechanism(queue.Queue):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def insert(self, data):
        with self.lock:
            self.put(data)


class ChatServer(LockingMechanism):
    def __init__(self):
        super().__init__()

        self.FORMAT = 'utf-8'
        self.host = None
        self.port = None
        self.client_threads = []
        self.client_socket = []
        self.isRunning = False
        self.SERVER = None

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def receive_client_msg(self, sock, addr):
        while True:
            data = sock.recv(1024).decode(self.FORMAT)
            if not data:
                print(f"{addr} is disconnected.")
                break
            data_list = {
                "address": addr,
                "msg": data
            }
            self.insert(data_list)
        # while True:
        #     data = sock.recv(1024).decode(FORMAT)
        #     if data:
        #         if mapping.is_exists(ip=addr[0]):
        #             name = mapping.get_name_with_ip(addr[0])
        #             print(f"{name}/: {data}")
        #         else:
        #             print(f"NEW CLIENT:[{addr}]/>: {data}")
        #
        #         if data.title() == "/Exit":
        #             sock.close()
        #             self.client_socket.remove(sock)
        #             print("client disconnected....")
        #             break
        # print(f"{addr} is disconnected")

    def handle_client(self, client_socket, addr):
        client_receive_thread = CThread(target=self.receive_client_msg, daemon=True, args=(client_socket, addr))
        client_receive_thread.start()

    def start_server(self):
        self.isRunning = True

        try:
            self.server_socket.listen()

            print(f"server is running: [{self.host}]:[{self.port}]")
            while self.isRunning:
                conn, addr = self.server_socket.accept()
                self.client_socket.append(conn)

                client_thread = CThread(target=self.handle_client, daemon=True, args=(conn, addr))
                client_thread.start()

                self.client_threads.append(client_thread)

        except Exception as e:
            print(f"an error is occured in server, error is: {e}")
        finally:
            self.isRunning = False

    def run(self):
        try:
            self.server_socket.bind((self.host, self.port))
        except Exception as e:
            print(f"error while binding: {e}")
            raise SocketBindingException("error while Binding")
        else:
            self.SERVER = CThread(target=self.start_server)
            self.SERVER.start()

    def Connect(self, host, port):
        self.host = host
        self.port = port

    def stop(self):
        print("client sockets: ")
        for client in self.client_socket:
            print(f"client: {client}")
            client.sendall("exit".encode(self.FORMAT))
            # try:
            #     client.close()
            # except Exception as e:
            #     pass

        print("client threads")
        for client_thread in self.client_threads:
            print(client_thread.is_alive(), end=", ")

        self.server_socket.close()
        self.isRunning = False
        self.SERVER.kill()
        print("server is closed")

    def isServerOnline(self):
        return self.isRunning


Server = ChatServer()

if __name__ == "__main__":
    # host = "127.0.0.1"
    host = "192.168.43.20"
    port = 65432

    server = ChatServer()
    server.Connect(host, port)
    server.run()
    time.sleep(20)
    server.stop()
