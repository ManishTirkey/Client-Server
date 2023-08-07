from IPmapping import mapping as c
from tkinter import ttk
from tkinter import font, messagebox as m_box
from tkinter import *
from CUSTOM_THREAD import thread_with_trace as CThread
from threading import Thread
from queue import Queue, Empty
import time

from ChatServer import Server as server
from Client import client as cs, ServerOffline
from IPmapping import ExistNameMappingException, ExistIPException

import psutil
from urllib import request

is_Online = "Offline"
DEFAULT_PORT = 65432
WORKING_THREADS_LIST = []


class CustomButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.left_canvas = Canvas(self, width=16, height=16, highlightthickness=0)
        self.left_canvas.pack(side=LEFT, padx=10, pady=2)

    def forget_canvas(self):
        self.left_canvas.grid_forget()

    def status(self, **kwargs):
        fill = kwargs['fill']
        if fill:
            self.left_canvas.create_oval(2, 2, 14, 14, fill=fill, outline=fill)
            self.left_canvas.pack(side=LEFT, padx=5, pady=2)


def Gray_btn():
    if prev_btn:
        prev_btn.status(fill="gray")


def close_client():
    cs.close()


def monitor_client_status():
    while not cs.isClosed:
        pass
    Gray_btn()


def close_current_client():
    close_client()
    chat_labelframe.configure(text="Chats")


def insertServerMsg(msg):
    msg_txt.tag_configure("red_tag", foreground="green")
    msg_txt.tag_configure("blue_tag", foreground="white")

    print(type(msg))
    print(msg)

    ip = msg['address'][0]
    name = c.get_name_with_ip(ip)

    msg_txt.configure(state=NORMAL)
    # msg_txt.insert(END, f"{str(msg['address'])}:/> ", "red_tag")
    msg_txt.insert(END, f"{name}/> ", "red_tag")
    msg_txt.insert(END, str(msg['msg']), "blue_tag")
    msg_txt.insert(END, "\n")
    # msg_txt.insert(END, msg['msg'])

    msg_txt.configure(state=DISABLED)


def monitorData():
    while is_Online != "Offline":
        try:
            msg = server.get_nowait()
        except Empty:
            pass
        else:
            insertServerMsg(msg)

        finally:
            clientNo = server.Total_clients()
            Client_no_label.configure(text=f"{clientNo}")


def online_offline():
    global is_Online
    state = ""

    # toggle is_Online
    # is_Online = (lambda: "Online", lambda: "Offline")[is_Online == "Online"]()
    msg_thread = CThread(target=monitorData, daemon=True)

    if is_Online == "Offline":

        adapter = Adapter_Combobox.get()
        host = str(ADAPTER_LIST[adapter])
        port = int(port_entry.get())

        try:

            server.Connect(host, port)
            server.run()

        except Exception as e:
            print(f"online_offline error is: {e}")
            m_box.showerror("Error", "Choose another Address")

        else:
            print("\t\t\tServer status offline")

            is_Online = "Online"
            state = "disable"

            listen_label.configure(
                text="Listening...", foreground="red", background="gray")
            Online.configure(text=is_Online, foreground="red")
            port_entry.configure(state='readonly')

            msg_thread.start()

    else:
        server.stop()
        is_Online = "Offline"
        state = "readonly"
        print("\t\t\tServer status offline")

        Online.configure(text=is_Online, foreground="black")
        listen_label.configure(
            text="Not Listening", foreground="black", background="#fff")
        port_entry.configure(state='normal')

        if msg_thread.is_alive():
            msg_thread.kill()

    Adapter_Combobox.configure(state=state)
    Connection_status.configure(text=is_Online)
    canvas.create_oval(1, 1, 13, 13, fill=STATUS[is_Online], outline=bg)


prev_btn = None  # store previous pressed btn, so that can change the color


def connect_to_ip(btn, ip):
    global prev_btn

    mcs = Thread(target=monitor_client_status, daemon=True)

    try:
        close_client()
        print(f"ip is: {ip}")
        cs.connect(str(ip), DEFAULT_PORT)

    except ServerOffline as e:
        m_box.showerror("Server", f"{e}")

    else:
        mcs.start()
        btn.status(fill="green")
        chat_labelframe.configure(text=f"{ip}")
        prev_btn = btn


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


def update_IP(ip):
    Selected_adapter_label.configure(text=ip)


win = Tk()
win.title("Local Area Network Chat")
win.geometry("1300x700+10+10")
win.minsize(1200, 700)
win.iconbitmap("icon.ico")
COLOR = "#DCDCDC"
win.configure(background=COLOR)

# -------------------styling

# normal style for client_button
style = ttk.Style(win)
style.configure("Custom.TButton", background="gray", foreground="black")

# styling after clicking
clicked_style = ttk.Style(win)
clicked_style.configure("ClickedCustom.TButton", background="green", foreground="black")

# -----------widgets------------

WIDGETS = Frame(win)
WIDGETS.pack(side=TOP, fill=X)

padx = 10
pady = 3

# -------------------------------------------------------------

top = Frame(win)
top.pack(fill=BOTH, expand=True, padx=10, pady=10)
top.configure(background="#DCDCDC")

top_panedwindow = PanedWindow(top, orient=HORIZONTAL, showhandle=True, background=COLOR)
top_panedwindow.pack(fill=BOTH, expand=True)

# ---------send
client_background = "#201d3e"


msg_frame = LabelFrame(top, text="Clients")
top_panedwindow.add(msg_frame)
msg_frame.configure(
    borderwidth=1,
    labelanchor=N,
    highlightthickness=0
)

conversation_canvas = Canvas(msg_frame, width=150)
conversation_canvas.pack(side=LEFT, fill="both", expand=True)

scroll_bar = Scrollbar(msg_frame, orient="vertical", command=conversation_canvas.yview)
scroll_bar.pack(side=RIGHT, fill=Y)
scroll_bar.config(background=COLOR)

# conversation_canvas.configure(yscrollcommand=scroll_bar.set)

content_frame = Frame(conversation_canvas, width=150)
conversation_canvas.create_window((0, 0), window=content_frame, anchor="nw")
content_frame.configure(
    borderwidth=0,
    highlightthickness=0
)


def Update_scroll_region():
    conversation_canvas.configure(scrollregion=conversation_canvas.bbox("all"))


content_frame.bind("<Configure>", lambda e: Update_scroll_region())
 

def ShowIP(btn, ip):
    win.title(f"{ip}")
    btn.after(10000, lambda: win.title("Local Area Network Chat"))


def delete_render():
    # print(content_frame.children) # all children in dict
    for btn in content_frame.winfo_children():  # all children inside list
        if btn.__class__ != ttk.Button().__class__:
            btn.grid_forget()
            btn.destroy()


client_btns = []


def render_clients():
    global client_btns
    client_btns.clear()

    clients = c.get_all_maps()

    for client in clients:
        client_btn = CustomButton(content_frame, text=client["name"])
        client_btn.pack(padx=10, pady=5, ipadx=50, ipady=6)
        client_btn.configure(command=lambda Cbtn=client_btn, ip=client["ip"]: connect_to_ip(Cbtn, ip))
        client_btn.status(fill="gray")

        client_btn.bind("<Button-3>", lambda e, cbtn=client_btn, ip=client['ip']: ShowIP(cbtn, ip))

        # client_btn.configure(style="Custom.TButton")
        client_btns.append(client_btn)
        Update_scroll_region()


close_client_btn = ttk.Button(content_frame, text="Close Connection")
close_client_btn.pack(padx=10, pady=5, ipadx=6, ipady=6)
close_client_btn.configure(command=lambda: close_current_client())


render_clients()

content_frame.update_idletasks()
conversation_canvas.configure(
    yscrollcommand=scroll_bar.set
)
Update_scroll_region()

# -------------------chat
chat_frame = Frame(top)
top_panedwindow.add(chat_frame)
chat_frame.configure(background="#fff")

# ----------------


def Connect():
    ip = ip_entry.get()
    name = name_entry.get()

    Exclude_list = [IP_PlaceHolder, NAME_PlaceHolder, ""]

    client = {}

    try:

        if ip not in Exclude_list and name == NAME_PlaceHolder:
            client['ip'] = ip
            client['name'] = ip

        elif ip not in Exclude_list and name != "":
            client['ip'] = ip
            client['name'] = name

        else:
            raise ValueError("Enter valid ip/name")

        c.insert(client)

    except ValueError as e:
        m_box.showerror("Value Error", f"{e}")

    except ExistIPException as e:
        m_box.showerror("IP Exist", f"{e}")

    except ExistNameMappingException as e:
        m_box.showerror("Name Exist", f"{e}")

    else:
        delete_render()
        render_clients()
        if checkbtn.get():
            connect_to_ip(client_btns[-1], ip)


connect_frame = LabelFrame(chat_frame, text="Connect-Remote")
connect_frame.configure(labelanchor=NW)
connect_frame.pack(side=TOP, fill=X)

IP_PlaceHolder = "Enter remote host IP:"
NAME_PlaceHolder = "suggest name for host: manish"
width = 40

ip_entry = ttk.Entry(connect_frame)
ip_entry.insert(0, IP_PlaceHolder)
ip_entry.grid(row=0, column=0, padx=(5, 10),pady=4)
ip_entry.configure(foreground="gray", width=width)

name_entry = ttk.Entry(connect_frame)
name_entry.insert(0, NAME_PlaceHolder)
name_entry.grid(row=0, column=1, padx=(10, 5), pady=4)
name_entry.configure(foreground="gray", width=width)

connect_button = ttk.Button(connect_frame, text="Connect")
connect_button.grid(row=0, column=2, pady=4)
connect_button.configure(command=Connect)

checkbtn = BooleanVar(value=False)
auto_connect = ttk.Checkbutton(connect_frame, variable=checkbtn, text="Auto Connect")
auto_connect.grid(row=0, column=3, padx=(15, 0))

ip_entry.bind("<FocusIn>", lambda e: on_focus_in(ip_entry, IP_PlaceHolder))
ip_entry.bind("<FocusOut>", lambda e: on_focus_out(ip_entry, IP_PlaceHolder))

name_entry.bind("<FocusIn>", lambda e: on_focus_in(name_entry, NAME_PlaceHolder))
name_entry.bind("<FocusOut>", lambda e: on_focus_out(name_entry, NAME_PlaceHolder))

# ----------------

# ---- chat label Frame

# chat_labelframe = LabelFrame(top, text="Chats", width=700)
chat_labelframe = LabelFrame(chat_frame, text="Chats", width=700)
# top_panedwindow.add(chat_labelframe)
chat_labelframe.pack(side=TOP, fill=BOTH, expand=True)
chat_labelframe.configure(background=COLOR,
                          highlightthickness=0,
                          labelanchor=N,
                          borderwidth=0,
                          )

scroll_chat = ttk.Scrollbar(chat_labelframe)
scroll_chat.pack(side=RIGHT, fill=Y)

msg_txt = Text(chat_labelframe)
scroll_chat.configure(command=msg_txt.yview)

msg_txt.pack(fill=BOTH, expand=True)
msg_txt.configure(width=10, wrap="word", state=DISABLED, yscrollcommand=scroll_chat.set)
msg_txt.configure(background="#1D1D39")
# --------------
MSG_PlaceHolder = "Enter Your Msg"


def on_focus_in(element, placeholder):
    if element.get() == placeholder:
        element.delete(0, "end")
        element.config(foreground='black')


def on_focus_out(element, placeholder):
    if element.get() == "":
        element.insert(0, placeholder)
        element.config(foreground='grey')


def sendTxt():
    msg = sendingTxt.get()
    try:
        cs.send(msg)

    except Exception as e:
        m_box.showinfo("Server", f"{e}")

    else:
        sendingTxt.delete(0, END)

        msg_txt.tag_configure("red_tag", foreground="green")
        msg_txt.tag_configure("blue_tag", foreground="white")

        msg_txt.configure(state=NORMAL)

        msg_txt.insert(END, "YOU:/> ", "red_tag")
        msg_txt.insert(END, f"{msg}", "blue_tag")
        msg_txt.insert(END, "\n")

        msg_txt.configure(state=DISABLED)


sendingFrame = LabelFrame(chat_labelframe, text="send your msg", labelanchor=NE)
sendingFrame.pack(side=BOTTOM, fill=X)

sendingTxt = Entry(sendingFrame)
sendingTxt.configure(width=100)
sendingTxt.insert(0, MSG_PlaceHolder)
sendingTxt.config(foreground="grey")
sendingTxt.pack(side=LEFT, pady=10, padx=(10, 0), ipady=10, ipadx=10)

send_btn = ttk.Button(sendingFrame, text="Send")
send_btn.pack(side=RIGHT, padx=(0, 10))
send_btn.configure(command=lambda: sendTxt())

sendingTxt.bind("<FocusIn>", lambda e: on_focus_in(sendingTxt, MSG_PlaceHolder))
sendingTxt.bind("<FocusOut>", lambda e: on_focus_out(sendingTxt, MSG_PlaceHolder))

win.bind("<Control-Return>", lambda e: sendTxt())

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

# -------------------new chat starting

def new_client():
    ip_placeholder = "Enter computer's ip address"
    name_placeholder = "Enter client name"

    def on_focus_in(element, placeholder):
        if element.get() == placeholder:
            element.delete(0, "end")
            element.config(foreground='black')

    def on_focus_out(element, placeholder):
        if element.get() == "":
            element.insert(0, placeholder)
            element.config(foreground='grey')

    new_client_gui = Toplevel()
    new_client_gui.title("New Chat")
    new_client_gui.minsize(450, 200)
    new_client_gui.maxsize(450, 200)
    # new_client_gui.geometry("450x200+50+50")

    # pop up in the center of main window
    new_client_gui.geometry(
        "+%d+%d" % (win.winfo_rootx() + win.winfo_width() // 2 - new_client_gui.winfo_reqwidth() // 2,
                    win.winfo_rooty() + win.winfo_height() // 2 - new_client_gui.winfo_reqheight() // 2))

    new_client_gui.transient(win)

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
    ip_entry.config(foreground='grey')

    Label(client_info_frame, text="Name: ").grid(row=1, column=0, sticky=W, pady=5, padx=(10, 20))
    name_entry = ttk.Entry(client_info_frame)
    name_entry.insert(0, name_placeholder)
    name_entry.grid(row=1, column=1, pady=5, ipadx=60, sticky=W)
    name_entry.config(foreground='grey')

    ip_entry.bind("<FocusIn>", lambda e: on_focus_in(ip_entry, ip_placeholder))
    ip_entry.bind("<FocusOut>", lambda e: on_focus_out(ip_entry, ip_placeholder))

    name_entry.bind("<FocusIn>", lambda e: on_focus_in(name_entry, name_placeholder))
    name_entry.bind("<FocusOut>", lambda e: on_focus_out(name_entry, name_placeholder))
    new_client_gui.bind("<Return>", lambda e: ok())

    # ---------------------

    def ok():
        # new_client_gui.grab_set()

        ip_placeholder = "Enter computer's ip address"
        name_placeholder = "Enter client name"

        ip = ip_entry.get()
        name = name_entry.get()

        Exclude_list = [ip_placeholder, name_placeholder, ""]

        if ip not in Exclude_list and name not in Exclude_list:
            client = {
                'ip': ip,
                'name': name,
            }
            try:
                c.insert(client)
            except Exception as e:
                m_box.showerror("Error", "IP/Name Already Exists")
            else:
                Exit()
                delete_render()
                render_clients()

            finally:
                # new_client_gui.grab_release()
                pass

    def Exit():
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
    cancel_btn.configure(command=Exit)

    # new_client_gui.protocol("WM_DELETE_WINDOW", Exit) # executes Exit function after clicking window close btn

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

Adapter_Combobox = ttk.Combobox(left_frame, state='readonly')
Adapter_Combobox.grid(row=0, column=1, padx=8)
Adapter_Combobox.configure(width=35)

Adapter_Combobox.bind("<<ComboboxSelected>>", lambda a: update_IP(ADAPTER_LIST[Adapter_Combobox.get()]))

Selected_adapter_label = Label(left_frame)
Selected_adapter_label.grid(row=0, column=2, padx=8)
Selected_adapter_label.configure(background=COLOR)

right_frame = Frame(frame)
right_frame.pack(side=RIGHT)
right_frame.configure(background=COLOR)

new_client_btn = ttk.Button(right_frame, text="New Chat")
new_client_btn.grid(row=0, column=0, padx=(0, 50))
new_client_btn.configure(command=new_client, state=DISABLED)


def Close():
    if is_Online == "Online":
        online_offline()

    close_client()
    win.destroy()


win.protocol("WM_DELETE_WINDOW", Close)

adapter_check_Thread = Thread(target=Check_Adapters, daemon=True, args=(Adapter_Combobox,))
adapter_check_Thread.start()
WORKING_THREADS_LIST.append(adapter_check_Thread)

win.mainloop()
