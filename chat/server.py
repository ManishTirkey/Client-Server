import socket
import threading
from _Colors_ import colors
import select
from threading import Thread

# HOST = "127.0.0.1"
# PORT = 65432
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# with server as s:
#     s.bind((HOST, PORT))
#     print("listening for connections....")
#     s.listen()
#     conn, addr = s.accept()
#     with conn as c:
#         print(f"Connected to: {addr[0]}, port: {addr[1]}")
#         msg = "welcome to my sever!"
#         c.sendall(msg.encode("utf-8"))
#
#         while True:
#             data = c.recv(2048)
#             if data.lower() == "exit":
#                 break
#             print(f"<{addr[0]}>: {data}")


# ---------------------------

# HOST = socket.gethostbyname(socket.gethostname())
HOST = "192.168.217.190"
PORT = 65432
ADDR = (HOST, PORT)
HEADER = 64
FORMAT = 'utf-8'
SERVER_CLOSE = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

print(f"{colors.bold} Server listening on: {ADDR} {colors.reset}")
server.listen()


# ----------------------
def Users(conn, addr):
    dis_msg = ""
    msg = f"Welcome user {str(addr)}"
    conn.sendall(msg.encode("utf-8"))
    CONNECTED = True
    ADDRESS = addr[0]
    CLIENT_PORT = addr[1]
    while CONNECTED:
        message = conn.recv(1024).decode(FORMAT)
        if message:
            pr_msg = f"{colors.fg.black}[{str(ADDRESS)}, {str(CLIENT_PORT)}]{colors.reset}{colors.bold}:{colors.reset} {colors.fg.green}{str(message)} {colors.reset}"
            if message.lower() == "exit":
                print(pr_msg)
                dis_msg = f"\n{colors.fg.red}User {addr} Disconnected.....{colors.reset}"
                conn.close()
                CONNECTED = False
                break
            print(pr_msg)
    print("client disconnected....")
    print(dis_msg)


# ----------------------

while not SERVER_CLOSE:
    print(f"waiting for new connections...")
    conn, addr = server.accept()
    
    print(f"\n{colors.fg.black}[NEW CONNECTION {addr}], CONNECTED to the Server")

    user_thread = Thread(target=Users, args=(conn, addr,))
    user_thread.start()

    print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1} {colors.reset}")
