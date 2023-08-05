import socket
import time
import threading

SERVER_HOST = "127.0.0.1"
# SERVER_HOST = "192.168.43.20"

PORT = 65432

ADDR = (SERVER_HOST, PORT)
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# def connect_to_server(ADDR):
#     try:
#         with client_socket as cs:
#             cs.connect(ADDR)
#
#             CONNECTED = True
#             while CONNECTED:
#                 msg = input(f"[You]:")
#                 try:
#                     cs.sendall(msg.encode("utf-8"))
#                     if msg.title() == "/Exit":
#                         print(f"Disconnected....")
#                         cs.close()
#                         break
#                 except Exception as e:
#                     print(f"error is: {e}")
#                     break
#     except Exception as e:
#         print(f"error is: {e}")
#

# connect_to_server(ADDR)

class ServerOffline(Exception):
    pass


class Client:
    def __init__(self):
        self.client_socket = None
        self.server = None
        self.port = None
        self.ADDR = None
        self.FORMAT = "utf-8"
        self.isClosed = True

    def connect(self, server, port):
        self.server = server
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)

        self.ADDR = (self.server, self.port)

        try:

            # with self.client_socket as self.CONNECTION:
            self.client_socket.connect(self.ADDR)

            print(f"client {self.ADDR} connected to server")

        except Exception as e:
            print(f"server is not Turned on: {e}")
            raise ServerOffline("server isn't listening")

        else:
            self.isClosed = False
            receiver_thread = threading.Thread(target=self.receiveMsgExit, daemon=True)
            receiver_thread.start()

    def receiveMsgExit(self):
        try:
            msg = self.client_socket.recv(1024).decode(self.FORMAT)
            if msg == "exit":
                self.isClosed = True
                self.client_socket.close()
        except:
            print("error on receiveMsgExit")

    def send(self, msg):
        try:
            self.client_socket.sendall(msg.encode(self.FORMAT))
        except Exception as e:
            print("server is disconnected")
            raise ServerOffline("server is Offline/Disconnected")

    def close(self):
        try:
            if not self.isClosed:
                self.client_socket.close()
        except Exception as e:
            print(f"connection is closed by remote host")
        else:
            self.isClosed = True
            print("You disconnected with server")


client = Client()

if __name__ == '__main__':
    cs = Client()
    cs.connect("127.0.0.1", 65432)
    print("msg auto send in 10secs")
    time.sleep(10)
    cs.send("hello manish")
    time.sleep(20)
    cs.close()

# --------------------------------------both end can send and receive data via single socket

# import socket
# import threading
#
#
# def receive_data(sock):
#     while True:
#         data = sock.recv(1024).decode("utf-8")
#         if not data:
#             break
#
#         print(f"\n\>: {data.decode()}", end="\n")
#         print("Enter a Msg: ")
#
#
# def run_client():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(("localhost", 8000))
#     print("Connected to server.")
#
#     # Start a separate thread to receive server messages
#     receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
#     receive_thread.start()
#
#     # Main thread for client input and sending messages to server
#     while True:
#         message = input("Enter a message: ")
#         client_socket.sendall(message.encode())
#
#         if message.lower() == "exit":
#             break
#
#     # Wait for the receive thread to complete
#     receive_thread.join()
#
#     client_socket.close()
#
#
# if __name__ == "__main__":
#     run_client()


# ------------------------------------------------

# import socket
# import threading
# import time
#
# SOCKET = None
#
#
# def receive_data(sock):
#     while True:
#         data = sock.recv(1024).decode("utf-8")
#         if not data:
#             break
#
#
# def run_client():
#     global SOCKET
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(("localhost", 8000))
#     print("Connected to server.")
#
#     SOCKET = client_socket
#
#     receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
#     receive_thread.start()
#
#     # while True:
#     #     message = input("Enter a message: ")
#     #     client_socket.sendall(message.encode())
#     #
#     #     if message.lower() == "exit":
#     #         break
#     #
#     # receive_thread.join()
#     #
#     # client_socket.close()
#     time.sleep(20)
#     SOCKET.sendall("hello mansih SKJDFHKJ".encode('utf-8'))
#
#
# def send_msg():
#     time.sleep(20)
#     SOCKET.sendall("hello mansih".encode('utf-8'))
#
#
# if __name__ == "__main__":
#     run_client()
#     send_msg()


# ----------------------------------------------------------
#
# import socket
# import threading
# import time
#
# SOCKET = None
#
#
# def receive_data(sock):
#     while True:
#         data = sock.recv(1024).decode()
#         if not data:
#             break
#
#
# def connectServer(host="localhost", port=8000):
#     global SOCKET
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((host, port))
#     print("Connected to server.")
#
#     SOCKET = client_socket
#
#     receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
#     receive_thread.start()
#
#
# def send_msg():
#     if SOCKET:
#         SOCKET.sendall("hello mansih".encode('utf-8'))
#
#
# connectServer()


# --------------------------------------
