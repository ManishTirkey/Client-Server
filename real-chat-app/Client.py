import socket
import time

SERVER_HOST = "0.0.0.0"
PORT = 12345

ADDR = (SERVER_HOST, PORT)
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_to_server(ADDR):

    with client_socket as cs:
        cs.connect(ADDR)

        CONNECTED = True
        while CONNECTED:
            msg = input(f"[You]:")
            cs.sendall(msg.encode("utf-8"))
            if msg.title() == "/Exit":
                print(f"Disconnected....")
                cs.close()
                break


connect_to_server(ADDR)

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