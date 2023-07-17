import socket
from threading import Thread
from tkinter import ttk
import tkinter as tk
from tkinter import *

win = tk.Tk()
win.geometry("1200x650+0+0")
win.title("server Listening.....")

FORMAT = 'utf-8'

SERVER_HOST = "192.168.43.5"
SERVER_PORT = 65432
SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

HEADER = 64
SERVER_CLOSE = False


def Users(conn, addr):
    dis_msg = ""

    CONNECTED = True
    ADDRESS = addr[0]
    CLIENT_PORT = addr[1]
    while CONNECTED:
        message = conn.recv(1024).decode(FORMAT)
        if message:
            pr_msg = f"[{str(ADDRESS)}, {str(CLIENT_PORT)}]: {str(message)} "
            if message.lower() == "exit":
                print(pr_msg)
                insert_msg(pr_msg)
                dis_msg = f"\nUser {addr} Disconnected....."
                conn.close()
                CONNECTED = False
                break
            print(pr_msg)
            insert_msg(pr_msg)
    print(dis_msg)
    insert_msg(dis_msg)


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(SERVER_ADDR)

    print(f"Server listening on: {SERVER_ADDR}")
    server.listen()

    try:
        while not SERVER_CLOSE:
            print(f"waiting for new connections...")
            conn, addr = server.accept()
            print(f"\n[NEW CONNECTION {addr}], CONNECTED to the Server")
            user_thread = Thread(target=Users, args=(conn, addr,))
            user_thread.start()
            # print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")
    except:
        exit(0)


def insert_msg(message=None):
    if msg is not None:
        text.insert(END, f"\n{message}")


# -------------------------------------------
CONNECTION = None


def connect_to_server():
    global CONNECTION
    serv_addr = (str(dist_entry.get()), int(dist_port_entry.get()))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # with server_socket as sc:
    server_socket.connect(serv_addr)
        # sc.connect(serv_addr)
    insert_msg(f"connected to server: {server_socket}")
    CONNECTION = server_socket


def connectToServer():
    Thread(target=connect_to_server).start()


def SendMsg():
    MESSAGE = msg_entry.get()
    CONNECTION.sendall(MESSAGE.encode(FORMAT))
    insert_msg(f"[YOU]: {MESSAGE}")
    if MESSAGE.lower() == "exit":
        CONNECTION.close()


clients = Frame(win)
clients.pack(side=LEFT, fill=BOTH, expand=True)

dist_addr = Label(clients, text="enter server Address: ")
dist_addr.grid(row=0, column=0, sticky=W, padx=(5, 10), pady=10)

dist_entry = Entry(clients)
dist_entry.grid(row=0, column=1, sticky=E, ipadx=30)

dist_port = Label(clients, text="port: ")
dist_port.grid(row=1, column=0, sticky=W, padx=(5, 10), pady=10)

dist_port_entry = Entry(clients)
dist_port_entry.grid(row=1, column=1, sticky=E, ipadx=30)

connect = ttk.Button(clients, text="Connect")
connect.grid(row=2, column=1, sticky=E)
connect.configure(command=connectToServer)

msg_entry = Entry(clients)
msg_entry.grid(columnspan=2, row=4, column=0, ipadx=40, pady=(10, 3), ipady=5)

send = ttk.Button(clients, text="Send")
send.grid(row=5, column=1, sticky=E)
send.configure(command=SendMsg)

# ---------------------------------------------------------msg

msg = Frame(win)
msg.pack(side=RIGHT, fill=BOTH, expand=True)

text = Text(msg)
text.pack(side=TOP, fill=BOTH, expand=True)

# --------------------------------------------------------

status_frame = Frame(win)
status_frame.pack(side=BOTTOM, fill=X)
status_frame.configure(background="#DBD9D9")

server_addr = Label(status_frame, text=f"server address: {SERVER_HOST},  port: {SERVER_PORT}", font="Arial 10")
server_addr.grid(row=0, column=0, sticky=W, padx=(10, 0), pady=3)
server_addr.configure(background="#DBD9D9", foreground="#7A6D6D")

server_thread = Thread(target=start_server)
server_thread.start()

win.mainloop()
