import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200")

# Create a LabelFrame
label_frame = ttk.LabelFrame(root, text="Data", height=150, width=250)
label_frame.pack(padx=10, pady=10)

# Create a Canvas inside the LabelFrame
canvas = tk.Canvas(label_frame, height=150, width=250)
canvas.pack(side="left", fill="both", expand=True)

# Create a Scrollbar
scrollbar = ttk.Scrollbar(label_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the Canvas to use the Scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a Frame inside the Canvas to hold the content
content_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Add content to the content_frame (example with Labels)
for i in range(20):
    label = ttk.Label(content_frame, text=f"Label {i+1}")
    label.pack(pady=5)

# Configure the Canvas scroll region
content_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

root.mainloop()
