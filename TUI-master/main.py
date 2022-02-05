import tkinter as tk
import math, sys, os, time, serial, struct
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from collections import namedtuple
from textboxwidget import TextBox



"""radio = serial.Serial('COM4', 9600)
STRUCT_SIZE = 56
MAGIC = 0xBEEFF00D

DARRELData_raw = struct.Struct('< I f f f f f f f f f d d') # 1 int 9 floats 2 doubles
DARRELData = namedtuple('DARRELData', [
   'magic',
   'time',
   'latitude',
   'longitude',
   'altitude',
   'accx',
   'accy',
   'accz',
   'mA',
   'V',
   'temp',
   'pressure'
])"""


class GroundComputer(tk.Frame):
    """ host = config.HOST
        port = config.PORT
        username = config.USERNAME
        password = config.PASSWORD"""
    width, height = 10,20

    @classmethod
    def main(cls):
        tk.NoDefaultRoot()
        root = tk.Tk()
        root.title("Ground Computer")
        root.geometry("1100x630+30+30")
        #root.configure(bg="#233342")
        cls(root).grid(sticky="nsew")
        root.minsize(1100, 680)
        root.maxsize(1100, 680)
        root.mainloop()

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.data = data
        self.connectionButton = tk.Button(
            self,
            text="Initialize Connection",
            command=self.initialize_connection,
        )
        self.plotButton = tk.Button(self, text="Plot", command=self.textPlot)
        self.statusLabel = tk.Label(self, text="", fg="red", bg="#233342")

        self.grid_widgets(padx=10, pady=10)

    def grid_widgets(self, **kw):
        self.connectionButton.grid(row=0, column=0, sticky="nsew", **kw)
        self.plotButton.grid(row = 0, column = 1, sticky = "nsew", **kw)
        self.statusLabel.grid(row=0, column=1, **kw)

    def textPlot(self):
        dataLabel = ["Magic","Time", "Latitude", "Longtidude", "altitude", "Accx", "accy", "MA", "V","Temperature", "Pressure"]
        textboxes = [None] * len(dataLabel)
        for i in range(0, len(dataLabel)):
            textboxes[i] = TextBox(self.data,dataLabel[i])
            textboxes[i].grid(column = i, row = 0)

    """def plot(self):
        dataLabel = ["Temperature", "Pressure", "Altitude"]
        fig = [None] * 3
        plotter = [None] * 3
        #y = [i ** 2 for i in range(20)]
        for i in range(0, len(dataLabel)):
            fig[i] = Figure(figsize=(3, 3), dpi=100)
            plotter[i] = fig[i].add_subplot(111)
            fig[i].suptitle(str(dataLabel[i]) + " vs time")
            #plot[i].plot(y)
            canvas = FigureCanvasTkAgg(fig[i], self)
            canvas.get_tk_widget().grid(row=1, column=i, sticky = 'nsew', pady = 10, padx = 20)
    """
    # initializes ssh connection to raspberry pi4 and executes command
    # still being developed
    def initialize_connection(self):
        pass
        """self.connectionButton.configure(state="disabled")
        # command = "cd Desktop/code/python3 main.py"
        command = "ls"
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, self.username, self.password)
        except SSHExepction:
            statusLabel.configure(text="Error", fg="red", bg="#233342")
    
        stdin, stdout, stderr = ssh.exec_command(command)
        print("success")
        self.statusLabel.configure(text="Success", fg="green", bg="#233342")"""



data = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

if __name__ == "__main__":
    GroundComputer.main(data)
    """try:
        while True:
            message = radio.read(STRUCT_SIZE)
            raw = DARRELData_raw.unpack(message)
            data = DARRELData(*raw)
            GroundComputer.main(data)
            if data.magic != MAGIC:
                print('INVALID MAGIC')
                radio.read(1)
            print(data)
            #time.sleep(0.5)
    except KeyboardInterrupt:
        radio.close()"""
