from IPmapping import mapping as c
import tkinter as tk
from tkinter import ttk
from tkinter import font, messagebox as m_box, colorchooser as cc
from tkinter import *

from CUSTOM_THREAD import thread_with_trace
from threading import Thread
import time

import psutil
import socket
from urllib import request

is_Online = False

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

for i in range(50):
    label = ttk.Button(content_frame, text=f"Label {i+1}")
    label.pack(pady=1)

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
canvas.create_oval(1, 1, 13, 13, fill="red", outline=bg)

Connection_status = Label(level_2l, text=is_Online)
Connection_status.grid(row=0, column=1)
Connection_status.configure(background=bg)

# --------------------level_1l

port_label = Label(level_1l, text="Port: ")
port_label.grid(row=0, column=1)
port_label.config(background=bg)

port_entry = ttk.Entry(level_1l)
port_entry.grid(row=0, column=2)
port_entry.insert(0, str(777))

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


# ------------

frame = Frame(win)
frame.pack(side=BOTTOM, fill=X)
frame.configure(background=COLOR)

Online = Button(frame, text="SERVER")
Online.grid(row=0, column=0, padx=8, pady=2)

Adapter_Combobox = ttk.Combobox(frame)
Adapter_Combobox["value"] = ["adapter"]
Adapter_Combobox.current(0)
Adapter_Combobox.grid(row=0, column=1, padx=8, pady=2)
Adapter_Combobox.configure(state="readonly", width=35)


Selected_adapter_label = Label(frame, text="current_adapter")
Selected_adapter_label.grid(row=0, column=2, padx=8, pady=2)
Selected_adapter_label.configure(background=COLOR)


win.mainloop()
