import threading
import time
from threading import Thread
import tkinter as tk
from tkinter import ttk
from tkinter import *
import socket

# ------------------------------

# li = ["mango", "orange", "pineapple", "apple"]
# print(li)
# li.append("coconut")
# print(li)
# li.remove("orange")
# print(li)


# ------------------------------
#
# class CustomButton(ttk.Button):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)
#
#         self.left_canvas = tk.Canvas(self, width=16, height=16, highlightthickness=0)
#         self.left_canvas.create_oval(2, 2, 14, 14, fill="white")
#         self.left_canvas.pack(side=tk.LEFT, padx=10, pady=2)
#
#     def forget_canvas(self):
#         self.left_canvas.grid_forget()
#
#     def status(self, **kwargs):
#         fill = kwargs['fill']
#         if fill:
#             self.left_canvas.create_oval(2, 2, 14, 14, fill=fill, outline=fill)
#             self.left_canvas.pack(side=tk.LEFT, padx=5, pady=2)
#

#
# root = tk.Tk()
# root.title("Custom Button Example")
#
#
# def on_button_click():
#     print("Button clicked!")
#
#
# custom_button = CustomButton(root, text="Click me", command=on_button_click, )
# custom_button.pack(padx=10, pady=10, ipadx=50, ipady=6)
# custom_button.status(fill="red")
# root.after(5000, lambda : custom_button.status(fill="green"))
# root.after(8000, lambda : custom_button.status(fill="yellow"))
# root.after(11000, lambda : custom_button.status(fill="blue"))
#
# root.mainloop()


# -------------------------------------


# def is_port_free(port):
#     try:
#         # Create a socket with the given port number
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.bind(('localhost', port))
#         return True
#     except OSError:
#         # Port is not free or other error occurred
#         return False
#
# port_to_check = 8080
#
# if is_port_free(port_to_check):
#     print(f"Port {port_to_check} is free.")
# else:
#     print(f"Port {port_to_check} is not free.")
#
#
# if is_port_free(port_to_check):
#     print(f"Port {port_to_check} is free.")
# else:
#     print(f"Port {port_to_check} is not free.")


# ----------------------

# def is_port_free(port):
#     try:
#         result = socket.getaddrinfo('localhost', port, socket.AF_UNSPEC, socket.SOCK_STREAM)
#         print(result)
#         return not any(result)
#     except socket.error:
#         return True


def is_port_free(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(s)
    result = s.connect_ex(('localhost', port))
    print(result)
    return result != 0


print(is_port_free(65432))
