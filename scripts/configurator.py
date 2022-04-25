import tkinter as tk
from tkinter import ttk
import threading
from PIL import ImageTk, Image
from pandas import Interval
from serial_arduino_functions import sendMsg

class App(threading.Thread):

    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.serial_port = serial_port
        self.start()
        self.ReadVals()
        self.yPad = 30

    def callback(self):
        self.root.quit()

    def onConfig(self):
        sendMsg(self.serial_port, "c,")

    def onStop(self):
        sendMsg(self.serial_port, "s,")

    def onGo(self):
        sendMsg(self.serial_port, "g,")

    def getVals(self):
        self.p = self.pSlider.get()
        self.i = self.iSlider.get()
        self.d = self.dSlider.get()
        self.s = self.sSlider.get()
    
    def Save(self):
        with open("save.txt", "a") as f:
            f.write(str(self.p/167) + "," + str(self.i/500) + "," + str(self.d/167) + "," + str(self.s/500) + "\n")

    def ReadVals(self):
        f = open("save.txt",'r').readlines()
        print(len(f))
        if len(f) != 0:
            settings = f[-1].rstrip().split(",")
            self.p = float(settings[0])*500
            self.i = float(settings[1])*500
            self.d = float(settings[2])*500
            self.s = float(settings[3])*500
        else:
            self.p = self.i = self.d = self.s = 0
    
    def ReturnVals(self):
        return self.p/167, self.i/500, self.d/167, self.s/500

    def run(self):
        self.root = tk.Tk()
        self.root.title("Imagine Configurator")
        self.root.geometry("900x600")

        self.tabControl = ttk.Notebook(self.root)

        self.mainTab = ttk.Frame(self.tabControl)
        self.slidersTab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.mainTab, text = 'Main')
        self.tabControl.add(self.slidersTab, text='Sliders')
        self.tabControl.pack(expand=1, fill="both")

        self.label = tk.Label(self.mainTab)
        self.label.grid(row=0, column=0, columnspan=3, pady=20)

        self.startButton = tk.Button(self.mainTab, text="Start", command=self.onGo)
        self.stopButton = tk.Button(self.mainTab, text="Stop", command=self.onStop)
        self.configButton = tk.Button(self.mainTab, text="Config", command=self.onConfig)

        self.startButton.grid(row=1, column=0)
        self.stopButton.grid(row=1, column=1)
        self.configButton.grid(row=1, column=2)

        self.pSlider = tk.Scale(self.slidersTab, from_=0, to_=500, length=800, orient=tk.HORIZONTAL)
        self.iSlider = tk.Scale(self.slidersTab, from_=0, to_=500, length=800, orient=tk.HORIZONTAL)
        self.dSlider = tk.Scale(self.slidersTab, from_=0, to_=500, length=800, orient=tk.HORIZONTAL)
        self.sSlider = tk.Scale(self.slidersTab, from_=0, to_=500, length=800, orient=tk.HORIZONTAL)
        self.saveButton = tk.Button(self.slidersTab, text = 'Save', command=self.Save)

        self.pSlider.place(rely=0.15, relx=0.5, anchor=tk.CENTER)
        self.iSlider.place(rely=0.3, relx=0.5, anchor=tk.CENTER)
        self.dSlider.place(rely=0.5, relx=0.5, anchor=tk.CENTER)
        self.sSlider.place(rely=0.7, relx=0.5, anchor=tk.CENTER)
        self.saveButton.place(rely=0.85, relx=0.5, anchor=tk.CENTER)

        self.root.mainloop()

    def sendImage(self, resizedImage):
        img = ImageTk.PhotoImage(image=Image.fromarray(resizedImage))
        self.label.configure(image=img)
        self.label.image = img