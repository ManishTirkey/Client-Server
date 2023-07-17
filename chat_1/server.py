import tkinter as tk
from tkinter import ttk
from tkinter import *
import time
from tkinter import font, messagebox as m_box, colorchooser as cc

from threading import Thread
from CUSTOM_THREAD import thread_with_trace
import psutil
import socket
from urllib import request



WORKING_THREADS_LIST = []
RUN = True

FORMAT = "utf-8"
DEFAULT_PORT = 8002
CURRENT_ADAPTER = "Wi-Fi"
CURRENT_ADAPTER_VALUE = ""
CLIENT_NAME = "unidentified Person"

is_Online = "Offline"
IS_SYSTEM_ONLINE = ""


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
    global adapter_list_keys, adapter_list
    while RUN:
        try:
            if win.state() != 'normal':
                break
        except:
            break
        adapter_list = get_all_adapter()
        adapter_list_keys = [i for i in adapter_list.keys()]
        adapter_combobox['values'] = adapter_list_keys

        if adapter_combobox.get() not in adapter_list_keys:
            adapter_combobox.current(0)
            Change_adapter()
        Change_adapter()
        time.sleep(1)


def Is_system_online():
    global IS_SYSTEM_ONLINE
    url = "www.google.com"
    try:
        s = socket.create_connection(
              (url, 80), timeout=2)
        if s is not None:
            s.close()
        IS_SYSTEM_ONLINE = "Online"
    except:
        IS_SYSTEM_ONLINE = "Offline"
    internet_status.configure(image=INTERNET_STATUS[IS_SYSTEM_ONLINE])


def updata_Internet_status():
    i = 0
    while RUN:
        try:
            if win.state() == "normal":
                Is_system_online()
            if win.state() != "normal":
                break
        except:
            break
        time.sleep(1)


def Start_server():
    print(CURRENT_ADAPTER_VALUE)
    print(f"port is: {port_entry.get()}")
    listen_label.configure(text="Listening...")


def Close_server():
    listen_label.configure(text="Not Listening")


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
font_family_tuples = font.families()
font_size_list = [i for i in range(8, 31, 1)]

CURRENT_FONT_FAMILY_SEND = "Arial"
CURRENT_FONT_SIZE_SEND = 12
CURRENT_COLOR_SEND = "black"

CURRENT_FONT_FAMILY_CHAT = "Arial"
CURRENT_FONT_SIZE_CHAT = 12
CURRENT_COLOR_CHAT = "black"

# -------------------------------------------------------------

WIDGETS_Send = Frame(WIDGETS)
WIDGETS_Send.pack(side=LEFT, fill=X, expand=True)


def Update_Send():
    TEXT.configure(font=(CURRENT_FONT_FAMILY_SEND, CURRENT_FONT_SIZE_SEND))


def Update_Send_Family():
    global CURRENT_FONT_FAMILY_SEND
    CURRENT_FONT_FAMILY_SEND = font_family.get()
    Update_Send()


def Update_Send_Size():
    global CURRENT_FONT_SIZE_SEND
    CURRENT_FONT_SIZE_SEND = font_size.get()
    Update_Send()


def Change_send_font_color():
    global CURRENT_COLOR_SEND
    CURRENT_COLOR_SEND = cc.askcolor()[1]
    TEXT.configure(fg=CURRENT_COLOR_SEND)
    current_color_label_send.configure(bg=CURRENT_COLOR_SEND)
    print(CURRENT_COLOR_SEND)


# ----------font-families------

font_family = ttk.Combobox(WIDGETS_Send, state='readonly')
font_family['values'] = font_family_tuples
font_family.current(font_family_tuples.index("Arial"))
font_family.grid(row=0, column=0, sticky=W, padx=padx, pady=pady)

# ------------font-size---------

font_size = ttk.Combobox(WIDGETS_Send, state='readonly')
font_size.grid(row=0, column=1, sticky=W)
font_size.configure(width=10)
font_size['values'] = font_size_list
font_size.current(3)

# ----------------font_color-----

font_send_icon = tk.PhotoImage(file="./icons/font_color.png")
font_send_btn = ttk.Button(WIDGETS_Send, image=font_send_icon)
font_send_btn.grid(row=0, column=2, padx=padx, sticky=W)

# -----------------current-color-label---

current_color_label_send = Label(WIDGETS_Send)
current_color_label_send.grid(row=0, column=3, ipadx=6, ipady=0)
current_color_label_send.configure(bg=CURRENT_COLOR_SEND)

font_family.bind("<<ComboboxSelected>>", lambda a: Update_Send_Family())
font_size.bind("<<ComboboxSelected>>", lambda a: Update_Send_Size())
font_send_btn.configure(command=Change_send_font_color)

# -------------------------------------------chat----------------

WIDGETS_Chat = Frame(WIDGETS)
WIDGETS_Chat.pack(side=RIGHT, fill=X, expand=True)


def Update_chat():
    msg_txt.configure(font=(CURRENT_FONT_FAMILY_CHAT, CURRENT_FONT_SIZE_CHAT))


def Update_Chat_Family():
    global CURRENT_FONT_FAMILY_CHAT
    CURRENT_FONT_FAMILY_CHAT = font_family_chat.get()
    print("update family")
    Update_chat()


def Update_Chat_Size():
    global CURRENT_FONT_SIZE_CHAT
    CURRENT_FONT_SIZE_CHAT = font_size_chat.get()
    print("update size")
    Update_chat()


def Change_chat_font_color():
    global CURRENT_COLOR_CHAT
    CURRENT_COLOR_CHAT = cc.askcolor()[1]
    msg_txt.configure(fg=CURRENT_COLOR_CHAT)
    current_color_label_chat.configure(bg=CURRENT_COLOR_CHAT)
    print(CURRENT_COLOR_CHAT)


# -------------font_family for chat---------

font_family_chat = ttk.Combobox(WIDGETS_Chat, state='readonly')
font_family_chat['values'] = font_family_tuples
font_family_chat.current(font_family_tuples.index("Arial"))
font_family_chat.grid(row=0, column=0, sticky=W, padx=padx, pady=pady)

# -------------font_size-for chat--------

font_size_chat = ttk.Combobox(WIDGETS_Chat, state='readonly')
font_size_chat.grid(row=0, column=1, padx=padx, pady=pady)
font_size_chat.configure(width=10)
font_size_chat['values'] = font_size_list
font_size_chat.current(3)

# -------------font-color--------

font_color_chat = tk.PhotoImage(file="./icons/font_color.png")
font_color_chat_btn = ttk.Button(WIDGETS_Chat, image=font_color_chat)
font_color_chat_btn.grid(row=0, column=2, padx=padx, sticky=W)

# -----------------font-color-current

current_color_label_chat = Label(WIDGETS_Chat)
current_color_label_chat.grid(row=0, column=3, ipadx=6, ipady=0)
current_color_label_chat.configure(bg=CURRENT_COLOR_CHAT)

font_family_chat.bind("<<ComboboxSelected>>", lambda a: Update_Chat_Family())
font_size_chat.bind("<<ComboboxSelected>>", lambda a: Update_Chat_Size())
font_color_chat_btn.configure(command=Change_chat_font_color)

# ---------------------------------------------------------------------------------------------------

top = Frame(win)
top.pack(fill=BOTH, expand=True, padx=10, pady=10)
top.configure(background="#DCDCDC")

top_panedwindow = PanedWindow(top, orient=HORIZONTAL,
                              showhandle=True,
                              background=COLOR
                              )
top_panedwindow.pack(fill=BOTH, expand=True)

# ---------send
msg_frame = LabelFrame(top, text="Write ur msg....")
# msg_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))
top_panedwindow.add(msg_frame)
msg_frame.configure(background=COLOR)
msg_frame.configure(
    # highlightthickness=5,
    # border=10,
    borderwidth=0,
    labelanchor=N,
)

TEXT = Text(msg_frame, width=3, height=100)
scroll_bar = Scrollbar(msg_frame)
scroll_bar.pack(side=RIGHT, fill=Y)
scroll_bar.config(command=TEXT.yview, background=COLOR)

TEXT.pack(side=TOP, expand=True, fill=BOTH)
TEXT.configure(height=1, wrap="word", yscrollcommand=scroll_bar.set)
TEXT.configure(font=(CURRENT_FONT_FAMILY_SEND, CURRENT_FONT_SIZE_SEND))
TEXT.focus_set()

# ------------

button_frame = Frame(msg_frame)
button_frame.pack(side=BOTTOM, fill=X, padx=10, pady=(10, 0))
button_frame.configure(background=COLOR)


def ONLINE():
    global WORKING_THREADS_LIST
    global is_Online
    state = ""

    # is_Online = "Offline" if is_Online == "Online" else "Online"
    # is_Online = is_Online == "Online" and "Offline" or "Online"
    # is_Online = ("Online", "Offline")[is_Online == "Online"]
    # is_Online = {True: "Offline", False: "Online"}[is_Online == "Online"]
    is_Online = (lambda: "Online", lambda: "Offline")[is_Online == "Online"]()

    if is_Online == "Online":
        # start_server_thread = thread_with_trace(target=Start_server)
        # start_server_thread.start()
        # WORKING_THREADS_LIST.append(start_server_thread)
        Start_server()
        Online.configure(text=is_Online, foreground="red")
        state = 'disable'
        port_entry.configure(state="readonly")

    else:
        Close_server()
        Online.configure(text=is_Online, foreground="black")
        state = 'readonly'
        port_entry.configure(state="norrmal")
    Adapter_Combobox.configure(state=state)

    Connection_status.configure(text=is_Online)
    canvas.create_oval(1, 1, 13, 13, fill=STATUS[is_Online], outline=bg)


def GetText():
    data = TEXT.get(1.0, END)
    insert(data)
    # BroadCast_Msg()


frame = Frame(button_frame)
frame.pack(side=LEFT, anchor=W)
frame.configure(background=COLOR)

Online = Button(frame, text=is_Online)
Online.grid(row=0, column=0, padx=8, pady=2)
Online.config(command=ONLINE)

adapter_list = get_all_adapter()
adapter_list_keys = [i for i in adapter_list.keys()]


def Change_adapter():
    current_adapter()
    Selected_adapter_label.configure(text=CURRENT_ADAPTER_VALUE)


def current_adapter():
    global CURRENT_ADAPTER_VALUE
    adapter = Adapter_Combobox.get()
    CURRENT_ADAPTER_VALUE = adapter_list[adapter]


Adapter_Combobox = ttk.Combobox(frame)
Adapter_Combobox["value"] = adapter_list_keys
Adapter_Combobox.current(0)
Adapter_Combobox.grid(row=0, column=1, padx=8, pady=2)
Adapter_Combobox.configure(state="readonly", width=35)

Adapter_Combobox.bind("<<ComboboxSelected>>", lambda a: Change_adapter())

current_adapter()
Selected_adapter_label = Label(frame, text=CURRENT_ADAPTER_VALUE)
# Selected_adapter_label = Label(frame)
Selected_adapter_label.grid(row=0, column=2, padx=8, pady=2)
Selected_adapter_label.configure(background=COLOR)

send_button = ttk.Button(button_frame, text="SEND")
send_button.pack(side=RIGHT, anchor=E, padx=padx)
send_button.config(command=GetText)


# -------------------chat


def insert(msg):
    if len(msg) > 1:
        msg = f"<{CURRENT_ADAPTER_VALUE}> YOU:/> \n{msg}"
        msg_txt.config(state=NORMAL)
        msg_txt.insert(END, msg)
        msg_txt.config(state=DISABLED)
        msg_txt.yview("end")


chat_frame = LabelFrame(top, text="chats")
# chat_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(0, 8))
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
msg_txt.configure(font=(CURRENT_FONT_FAMILY_CHAT, CURRENT_FONT_SIZE_CHAT))

# ------------------- bottom - signature

bg = "#cfcfcf"
STATUS = {
    "Offline": "#757575",
    "Online": "#FF4900"
}

bottom = Frame(win)
bottom.pack(side=BOTTOM, fill=X)
bottom.configure(border=5, background=bg)

# ------------------level-1-RIGHT

level_1r = Frame(bottom)
level_1r.pack(side=RIGHT)
level_1r.configure(background=bg)

INTERNET_STATUS = {
    "Online": tk.PhotoImage(file="icons/online_3/online-24.png"),
    "Offline": tk.PhotoImage(file="icons/offline_1/offline-24.png")
}

internet_label = Label(level_1r, text="Internet Status: ")
# internet_label.grid(row=0, column=0)
# internet_label.configure(background=bg)

internet_status = Label(level_1r)
# internet_status.grid(row=0, column=1)
# internet_status.configure(background=bg)

sign_label = Label(level_1r, text="Manish Tirkey")
sign_label.grid(row=0, column=3, padx=(15, 2))
sign_label.configure(background=bg, font="Arial 10 bold")
# ---------------------level-2


# --------------------level_1---------LEFT

level_1l = Frame(bottom)
level_1l.pack(side=LEFT)
level_1l.config(background=bg)

# --------------------level_2l

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
port_entry.insert(0, str(DEFAULT_PORT))

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


def Close():
    global RUN
    global WORKING_THREADS_LIST
    close = m_box.askyesno("EXIT", "After Exit messages will be destroyed.")
    if close:
        if len(WORKING_THREADS_LIST) > 0:
            print("going to kill all threads")
            try:
                for i in WORKING_THREADS_LIST:
                    i.kill()
                    RUN = False
            except Exception as e:
                print(e)
        if is_Online == "Online":
            print("Turning off server")
            ONLINE()  # close the server if server is Running
        win.destroy()


win.protocol("WM_DELETE_WINDOW", Close)

adapter_check_Thread = thread_with_trace(target=Check_Adapters, args=(Adapter_Combobox,))
adapter_check_Thread.start()
WORKING_THREADS_LIST.append(adapter_check_Thread)

# check_internet_status = thread_with_trace(target=updata_Internet_status, args=())
# check_internet_status.start()
# WORKING_THREADS_LIST.append(check_internet_status)

win.mainloop()
