import socket

CLIENT_HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = "192.168.43.20"
PORT = 65432

sh = input(f"SERVER_HOST[{SERVER_HOST}]: ")
if sh:
    SERVER_HOST = sh
    print(f"[{sh}]")
else:
    print(f"Default[{SERVER_HOST}]")

port = input(f"PORT[{PORT}]: ")
if port:
    print(f"[{port}]")
else:
    print(f"Default[{PORT}]")

# -------------------------------------------

ADDR = (SERVER_HOST, PORT)
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_to_server():
    with client_socket as cs:
        cs.connect(ADDR)
        # print(cs)
        # data = cs.recv(2028).decode(FORMAT)
        # print(f"\n\t\t\tSOCKET IP: {CLIENT_HOST}")
        # print(f"{colors.fg.lightred}server:{colors.bold} {colors.fg.lightgreen}{data}{colors.reset}")

        CONNECTED = True
        while CONNECTED:
            msg = input(f"[You]: ")
            cs.sendall(msg.encode("utf-8"))
            if msg.lower() == "exit":
                print(f"Disconnected....")
                cs.close()
                CONNECTED = False


connect_to_server()

















#
#
# import socket
# from threading import Thread
#
# HOST = "192.168.43.5"
# PORT = 65431
# ADDR = (HOST, PORT)
# HEADER = 64
# FORMAT = 'utf-8'
# SERVER_CLOSE = False
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server.bind(ADDR)
#
# print(f"Server listening on: {ADDR}")
# server.listen()
#
#
# # ----------------------
# def Users(conn, addr):
#     dis_msg = ""
#     msg = f"Welcome user {str(addr)}"
#     conn.sendall(msg.encode("utf-8"))
#     CONNECTED = True
#     ADDRESS = addr[0]
#     CLIENT_PORT = addr[1]
#     while CONNECTED:
#         message = conn.recv(1024).decode(FORMAT)
#         if message:
#             pr_msg = f"[{str(ADDRESS)}, {str(CLIENT_PORT)}]: {str(message)}"
#             if message.lower() == "exit":
#                 print(pr_msg)
#                 dis_msg = f"\nUser {addr} Disconnected....."
#                 conn.close()
#                 CONNECTED = False
#                 break
#             print(pr_msg)
#     print("client disconnected....")
#     print(dis_msg)
#
#
# # ----------------------
#
# while not SERVER_CLOSE:
#     print(f"waiting for new connections...")
#     conn, addr = server.accept()
#     print(f"\n[NEW CONNECTION {addr}], CONNECTED to the Server")
#     user_thread = Thread(target=Users, args=(conn, addr,))
#     user_thread.start()
