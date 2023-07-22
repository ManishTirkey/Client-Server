from IPmapping import mapping as c
import tkinter as tk
from tkinter import ttk
from tkinter import font, messagebox as m_box, colorchooser as cc
from tkinter import *

from threading import Thread
import time

import psutil
import socket
from urllib import request

is_Online = "Offline"
DEFAULT_PORT = 8084
WORKING_THREADS_LIST = []


def start_server():
    pass


def close_server():
    pass


def online_offline():
    global is_Online
    state = ""

    is_Online = (lambda: "Online", lambda: "Offline")[is_Online == "Online"]()

    if is_Online == "Online":
        print("going to online server")
        Online.configure(text=is_Online, foreground="red")
        state = "disale"
        port_entry.configure(state='readonly')

    else:
        print("going to offline server")
        Online.configure(text=is_Online, foreground="black")
        state = "readonly"
        port_entry.configure(state='normal')

    Adapter_Combobox.configure(state=state)
    Connection_status.configure(text=is_Online)
    canvas.create_oval(1, 1, 13, 13, fill=STATUS[is_Online], outline=bg)


def connect_to_ip(IP):
    print(f"connecting to ip: {IP}")


def get_all_adapter():
    nics = {}
    result = psutil.net_if_addrs()
    for key in result.keys():
        adapter = result[key]
        for snicaddr in adapter:
            if snicaddr[0].value == 2:
                nics[key] = snicaddr[1]
    return nics


def Check_Adapters(adapter_combobox):
    global ADAPTER_LIST

    while True:
        try:
            if win.state() != 'normal':
                break
        except:
            break

        ADAPTER_LIST = get_all_adapter()
        ADAPTER_NAME_LIST = [i for i in ADAPTER_LIST.keys()]

        adapter_combobox['values'] = ADAPTER_NAME_LIST

        if adapter_combobox.get() not in ADAPTER_NAME_LIST:
            adapter_combobox.current(0)

        ip = ADAPTER_LIST[adapter_combobox.get()]
        update_IP(ip)
        time.sleep(1)


def update_IP(IP):
    Selected_adapter_label.configure(text=IP)


win = Tk()
win.title("Local Area Network Chat")
win.geometry("1200x600+50+50")
win.iconbitmap("icon.ico")
COLOR = "#DCDCDC"
win.configure(background=COLOR)

# -----------widgets------------

WIDGETS = Frame(win)
WIDGETS.pack(side=TOP, fill=X)

padx = 10
pady = 3

# -------------------------------------------------------------

top = Frame(win)
top.pack(fill=BOTH, expand=True, padx=10, pady=10)
top.configure(background="#DCDCDC")

top_panedwindow = PanedWindow(top, orient=HORIZONTAL,
                              showhandle=True,
                              background=COLOR
                              )
top_panedwindow.pack(fill=BOTH, expand=True)

# ---------send
msg_frame = LabelFrame(top, text="Clients")
top_panedwindow.add(msg_frame)
msg_frame.configure(
    background=COLOR,
    borderwidth=2,
    labelanchor=N,
    highlightthickness=0
)

conversation_canvas = Canvas(msg_frame, width=150)
conversation_canvas.pack(side=LEFT, fill="both", expand=True)

scroll_bar = Scrollbar(msg_frame, orient="vertical")
scroll_bar.pack(side=RIGHT, fill=Y)
scroll_bar.config(command=conversation_canvas.yview, background=COLOR)

content_frame = ttk.Frame(conversation_canvas, width=150)
conversation_canvas.create_window((0, 0), window=content_frame, anchor="nw")


def render_clients():
    for client in c.get_all_maps():
        label = ttk.Button(content_frame, text=client["name"])
        label.pack(pady=1)
        label.configure(command=lambda ip=client["ip"]: connect_to_ip(ip))


content_frame.update_idletasks()
conversation_canvas.configure(
    scrollregion=conversation_canvas.bbox("all"),
    yscrollcommand=scroll_bar.set
)

# -------------------chat

chat_frame = LabelFrame(top, text="chats", width=700)
top_panedwindow.add(chat_frame)
chat_frame.configure(background=COLOR,
                     highlightthickness=0,
                     labelanchor=N,
                     borderwidth=0,
                     )

scroll_chat = ttk.Scrollbar(chat_frame)
scroll_chat.pack(side=RIGHT, fill=Y)

msg_txt = Text(chat_frame)
scroll_chat.configure(command=msg_txt.yview)

msg_txt.pack(fill=BOTH, expand=True)
msg_txt.configure(width=10, wrap="word", state=DISABLED, yscrollcommand=scroll_chat.set)

# ------------------- bottom - signature

bg = "#cfcfcf"
STATUS = {
    "Offline": "#757575",
    "Online": "#FF4900"
}

bottom = Frame(win)
bottom.pack(side=BOTTOM, fill=X)
bottom.configure(border=5, background=bg)

# ------------------level-1-BOTTOM-RIGHT

level_1r = Frame(bottom)
level_1r.pack(side=RIGHT)
level_1r.configure(background=bg)

sign_label = Label(level_1r, text="Manish Tirkey")
sign_label.grid(row=0, column=3, padx=(15, 2))
sign_label.configure(background=bg, font="Arial 10 bold")
# ---------------------level-2


# --------------------level_1--BOTTOM-LEFT

level_1l = Frame(bottom)
level_1l.pack(side=LEFT)
level_1l.config(background=bg)

# --------------------level_2l --SERVER STATUS

level_2l = Frame(level_1l)
level_2l.grid(row=0, column=0, padx=(0, 30))
level_2l.configure(background=bg)

canvas = Canvas(level_2l, background=bg, width=14, height=14, border=0, highlightthickness=0)
canvas.grid(row=0, column=0)
canvas.create_oval(1, 1, 13, 13, fill=STATUS[is_Online], outline=bg)

Connection_status = Label(level_2l, text=is_Online)
Connection_status.grid(row=0, column=1)
Connection_status.configure(background=bg)

# --------------------level_1l

port_label = Label(level_1l, text="Port: ")
port_label.grid(row=0, column=1)
port_label.config(background=bg)

port_entry = ttk.Entry(level_1l)
port_entry.grid(row=0, column=2)
port_entry.insert(0, DEFAULT_PORT)

listen_label = Label(level_1l, text="Not Listening")
listen_label.grid(row=0, column=3, padx=(20, 10))
listen_label.configure(background=bg)

Client_label = Label(level_1l, text="Clients: ")
Client_label.grid(row=0, column=4)
Client_label.configure(background=bg)

Client_no_label = Label(level_1l, text="0")
Client_no_label.grid(row=0, column=5)
Client_no_label.configure(background=bg)


# --------------------level_1l

# -------------------new chat starting

def new_client():
    ip_placeholder = "Enter computer's ip address"
    name_placeholder = "Enter client name"

    def on_entry_click(element, placeholder):
        if element.get() == placeholder:
            element.delete(0, "end")
            element.config(foreground='black')

    def on_focus_out(element, placeholder):
        if element.get() == "":
            element.insert(0, placeholder)
            element.config(foreground='grey')

    new_client_gui = Toplevel()
    new_client_gui.title("New Chat")
    new_client_gui.geometry("450x200+50+50")
    new_client_gui.minsize(450, 200)
    new_client_gui.maxsize(450, 200)

    top_frame = Frame(new_client_gui)
    top_frame.pack(side=TOP, fill=BOTH, expand=True)

    heading = Label(top_frame, text="LAN Chat")
    heading.pack(side=TOP)
    heading.configure(font=('Arial Black', 32))

    client_info_frame = Frame(top_frame)
    client_info_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

    Label(client_info_frame, text="Computer's IP: ").grid(row=0, column=0, sticky=W, pady=5, padx=(10, 20))
    ip_entry = ttk.Entry(client_info_frame)
    ip_entry.insert(0, ip_placeholder)
    ip_entry.grid(row=0, column=1, ipadx=80, pady=5, sticky=W)

    Label(client_info_frame, text="Name: ").grid(row=1, column=0, sticky=W, pady=5, padx=(10, 20))
    name_entry = ttk.Entry(client_info_frame)
    name_entry.insert(0, name_placeholder)
    name_entry.grid(row=1, column=1, pady=5, ipadx=60, sticky=W)

    ip_entry.bind("<FocusIn>", lambda e: on_entry_click(ip_entry, ip_placeholder))
    ip_entry.bind("<FocusOut>", lambda e: on_focus_out(ip_entry, ip_placeholder))

    name_entry.bind("<FocusIn>", lambda e: on_entry_click(name_entry, name_placeholder))
    name_entry.bind("<FocusOut>", lambda e: on_focus_out(name_entry, name_placeholder))
    new_client_gui.bind("<Return>", lambda e: ok())

    # ---------------------

    def ok():
        ip_placeholder = "Enter computer's ip address"
        name_placeholder = "Enter client name"

        ip = ip_entry.get()
        name = name_entry.get()

        if ip != ip_placeholder and name != name_placeholder:
            client = {
                'ip': ip,
                'name': name,
            }
            try:
                c.insert(client)
            except Exception as e:
                m_box.showerror("Error", "IP/Name Already Exists")
            else:
                clients()
                exit()

    def exit():
        new_client_gui.destroy()

    bg = "#cfcfcf"
    bottom_frame = Frame(new_client_gui)
    bottom_frame.pack(side=BOTTOM, fill=X)
    bottom_frame.configure(pady=5, background=bg)

    bottom_right_frame = Frame(bottom_frame)
    bottom_right_frame.pack(side=RIGHT)

    ok_btn = ttk.Button(bottom_right_frame, text="Ok")
    ok_btn.grid(row=0, column=0)
    ok_btn.configure(command=ok)

    cancel_btn = ttk.Button(bottom_right_frame, text="Cancel")
    cancel_btn.grid(row=0, column=1)
    cancel_btn.configure(command=exit)

    new_client_gui.mainloop()


# ------------

frame = Frame(win)
frame.pack(side=BOTTOM, fill=X)
frame.configure(background=COLOR, pady=8)

left_frame = Frame(frame)
left_frame.pack(side=LEFT)
left_frame.configure(background=COLOR)

Online = Button(left_frame, text=is_Online)
Online.grid(row=0, column=0, padx=20)
Online.configure(command=online_offline)

Adapter_Combobox = ttk.Combobox(left_frame)
Adapter_Combobox.grid(row=0, column=1, padx=8)
Adapter_Combobox.configure(state="readonly", width=35)

Adapter_Combobox.bind("<<ComboboxSelected>>", lambda a: update_IP(ADAPTER_LIST[Adapter_Combobox.get()]))

Selected_adapter_label = Label(left_frame)
Selected_adapter_label.grid(row=0, column=2, padx=8)
Selected_adapter_label.configure(background=COLOR)

right_frame = Frame(frame)
right_frame.pack(side=RIGHT)
right_frame.configure(background=COLOR)

new_client_btn = ttk.Button(right_frame, text="New Chat")
new_client_btn.grid(row=0, column=0, padx=(0, 50))
new_client_btn.configure(command=new_client)


def Close():
    win.destroy()


win.protocol("WM_DELETE_WINDOW", Close)

adapter_check_Thread = Thread(target=Check_Adapters, daemon=True, args=(Adapter_Combobox,))
adapter_check_Thread.start()
WORKING_THREADS_LIST.append(adapter_check_Thread)

win.mainloop()
