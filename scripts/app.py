import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from hc_12_functions import *
from functools import partial

serial_port = getSerial()

root = tk.Tk()
root.title("HC-12 Test")
root.geometry("400x300")

tabControl = ttk.Notebook(root)

testTab = ttk.Frame(tabControl)
setupTab = ttk.Frame(tabControl)
  
tabControl.add(testTab, text ='Test')
tabControl.add(setupTab, text ='Setup')
tabControl.pack(expand = 1, fill ="both")

inputBox = ttk.Entry(testTab, width=48)
inputBox.pack(pady=1)

feed = scrolledtext.ScrolledText(testTab, wrap = tk.WORD, width = 48, height = 30)
feed.configure(state ='disabled')
feed.pack()

setupLabel = ttk.Label(setupTab, text = "Setup Mode")
setupLabel.pack(pady=20)

confirmLabelText = tk.StringVar()

def buttonCmd():
    setDefault(serial_port)
    feed.configure(state ='normal')
    feed.insert(tk.INSERT, "Sent: " + "AT+DEFAULT\n")
    feed.configure(state ='disabled')

button = ttk.Button(setupTab, text="Set Default", command=buttonCmd)
button.pack(pady=50)

confirmLabel = ttk.Label(setupTab, textvariable=confirmLabelText)
confirmLabel.pack(pady=20)

def get(event):
    msg = inputBox.get() + "\n"
    if msg != "\n":
        sendMsg(serial_port, msg)
        feed.configure(state ='normal')
        feed.insert(tk.INSERT, "Sent: " + msg)
        feed.configure(state ='disabled')
        inputBox.delete(0, tk.END)

def receive():
    msg = getMsg(serial_port)
    if msg != "":
        feed.configure(state='normal')
        feed.insert(tk.INSERT, "Received: " + msg)
        feed.configure(state ='disabled')
    feed.yview(tk.END)
    root.after(200, receive)

inputBox.bind('<Return>', get)

receive()

root.mainloop()