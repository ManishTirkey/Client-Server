import socket
import time

# import enum
# import ipaddress
# from ClientAdapters import Adapter

from _Colors_ import colors


CLIENT_HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = "127.0.0.1"
PORT = 65432

sh = input(f"SERVER_HOST{colors.fg.red}[{SERVER_HOST}]{colors.reset}: ")
if sh:
    SERVER_HOST = sh
    print(f"{colors.fg.green}[{sh}]{colors.reset}")
else:
    print(f"{colors.bold}Default{colors.reset}{colors.fg.green}[{SERVER_HOST}]{colors.reset}")

port = input(f"PORT{colors.fg.red}[{PORT}]{colors.fg.red}{colors.reset}: ")
if port:
    print(f"{colors.fg.green}[{port}]{colors.reset}")
else:
    print(f"{colors.bold}Default{colors.reset}{colors.fg.green}[{PORT}]{colors.reset}")

# -------------------------------------------

ADDR = (SERVER_HOST, PORT)
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_to_server(ADDR):
    with client_socket as cs:
        cs.connect(ADDR)
        print(cs)
        data = cs.recv(2028).decode(FORMAT)
        print(f"\n\t\t\tSOCKET IP: {CLIENT_HOST}")
        # print(f"{colors.fg.lightred}server:{colors.bold} {colors.fg.lightgreen}{data}{colors.reset}")

        time.sleep(5)
        print(f"server: {data}")

        if data == "exit":
            print("closing from client")
            cs.close()

        # while False:
        #     # msg = input(f"{colors.fg.black}[You]{colors.reset}{colors.bold}:{colors.reset}{colors.fg.green} ")
        #     msg = input(f"[You]: ")
        #
        #     if msg.lower() == "exit":
        #         # print(f"{colors.reset}{colors.fg.red}Disconnected....{colors.reset}")
        #         print(f"Disconnected....")
        #         cs.close()
        #         break
        #     print(f"sending msg: {msg}")
        #     cs.sendall(msg.encode("utf-8"))
        print("you are disconnected with server")


connect_to_server(ADDR)

