import tkinter as tk
from textboxwidget import TextBox
import tkinter.scrolledtext as tkscrolled
import serial, struct
from collections import namedtuple
import threading
import logging
import queue
import time
import math
from crccheck.crc import Crc32
from datetime import datetime

STRUCT_SIZE = 60
MAGIC = 0xBEEFF00D

DARRELData_raw = struct.Struct('< I f f f f f f f f f d d I') # 1 int 9 floats 2 doubles
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
'pressure',
'checksum'
])

def quit():
    root.quit()

class TUI(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        #TODO parse ARGV to get this args
        # if we have a value here, read from the file instead of the radio
        self.fname = "C:\\Users\\aaron\\Desktop\\TUI\\actualflightdata\\test data2.txt"

        self.dataLabel = [ "pres_alt","altitude", "latitude", "longitude", "time", "accx", "accy","accz", "mA", "V","temp", "pressure","magic"]
        self.unitLabel = ["[meters]", '[meters]', "","","[ms]","[m/s^2]", "[m/s^2]", "[m/s^2]", "[mA]", "[volts]", "[celcius]", "[pascal]",""]
        #change pres_alt to altitude change altitidue to gps alt
        self.parent = parent
        self.backgroundImage = tk.PhotoImage(file = "assets/resize_1.png")
        w = self.backgroundImage.width()
        h = self.backgroundImage.height()
        self.cv = tk.Canvas(width =self.winfo_screenwidth(), height = self.winfo_screenheight())
        self.connectionButton = tk.Button(
            self.cv,
            text="Initialize Connection",
            command=None, width = 17
        )
        self.plotButton = tk.Button(self.cv, text="Plot", command=lambda: self.textPlot(self.dataLabel), width = 17)
        self.statusLabel = tk.Label(self.cv, text="", fg="red", bg="#233342")
        self.closeButton = tk.Button(self.cv, text = "End Connection", command = self.close, width = 17, bg = 'red', fg = 'white')

        self.credit = tk.Label(self.cv, text = "RRPL 2021", fg = 'purple')
        #self.connectionButton.configure(state = 'disabled')
        #self.closeButton.configure(state = 'disabled')
        self.grid_widgets(padx=10, pady=10)


    def grid_widgets(self, **kw):
        self.cv.pack( fill = 'both', expand = 'yes')
        self.cv.create_image(350,550, image = self.backgroundImage, anchor = 'center')

        #self.connectionButton.grid(row=0, column=0, sticky="nsew", **kw)
        self.plotButton.grid(row = 0, column = 0, sticky = "nsew", **kw)
        #self.statusLabel.grid(row=7, column=1, **kw)
        self.closeButton.grid(row = 0, column = 1, sticky = 'nsew' ,**kw)
        self.credit.grid(row = 0, column = 5, sticky = 'nsew' ,**kw )


    def textPlot(self,dataLabel):
        self.plotButton.configure(state = 'disabled')
        date = datetime.now().isoformat()
        self.f = open(f'flightData-{date}.txt'.replace(':', '-'), 'w')
        width,height = 20,5
        #self.closeButton.configure(status = 'active')
        self.textboxes = [None] * len(dataLabel)
        self.outputLabels = [None] * len(dataLabel)
        for i in range(0, len(dataLabel)-1):
            if self.dataLabel[i] == "pres_alt":
                self.outputLabels[i] = tk.Label(self.cv, fg ='black', font = ('Droid serif', 12), text = "altitude " + self.unitLabel[i])
            elif self.dataLabel[i] == "altitude":
                self.outputLabels[i] = tk.Label(self.cv, fg ='black', font = ('Droid serif', 12), text = "GPS altitude " + self.unitLabel[i])
            else:
                self.outputLabels[i] = tk.Label(self.cv, fg ='black', font = ('Droid serif', 12), text = self.dataLabel[i] +" "+ self.unitLabel[i])

            self.textboxes[i] = tk.Label(self.cv,bg = 'black',font = ("Droid serif",12), fg = '#39FF14', width = 20, height = 5)
            if i>=4 and i <8:
                self.outputLabels[i].grid(column = i-4, row = 3)
                self.textboxes[i].grid(column = i-4, row = 4, padx = 10, pady=(2,10))
                continue
            elif i>=8:
                self.outputLabels[i].grid(column = i-8, row = 5, pady = 5)
                self.textboxes[i].grid(column = i-8, row = 6, padx = 10,pady=(2,10))
                continue

            self.outputLabels[i].grid(column = i, row = 1)
            self.textboxes[i].grid(column = i, row = 2,padx = 10,pady=(2,10) )

        x = threading.Thread(target=self.display)
        x.start()

    def setup_ui(self):
        # Autoscroll to the bottom
        self.tempLAT = "No GPS Fix"
        self.tempLON = "No GPS Fix"
        self.tempALT = "No GPS Fix"
        self.flag = True
        self.magicStatus = tk.Label(self.cv, text = "", font = ("Droid serif",20))
        self.magicStatus.grid(column = 1, row = 8, pady = 20)

        self.checksumStatus = tk.Label(self.cv, text = "", font = ("Droid serif", 20))
        self.checksumStatus.grid(column = 1, row = 9, pady = 10)

    def display(self):
        if self.fname:
            self.display_file()
        else:
            self.display_radio()

    def display_radio(self):
        self.radio = serial.Serial('COM4', 9600)

        self.setup_ui()

        while self.flag:
            message = self.radio.read(STRUCT_SIZE)
            raw = DARRELData_raw.unpack(message)
            msg = DARRELData(*raw)
            self.our_checksum = Crc32.calc(message[:STRUCT_SIZE - 4])
            if msg.magic != MAGIC or self.our_checksum != msg.checksum:
                self.radio.read(1)
                continue
            press_h = self.press_alt(msg)
            packet_string = ' '.join([str(v) for v in raw])
            self.f.write(packet_string + '\n')
            #print(press_h)
            self.handle_datapoint(
                msg, press_h,
                valid_checksum=self.our_checksum != msg.checksum,
                valid_magic=msg.magic == MAGIC
            )
            #print("looping")

    def display_file(self):
        f = open(self.fname)

        self.setup_ui()

        while self.flag:
            line = f.readline()
            raw = [float(x) for x in line.split(' ')]
            msg = DARRELData(*raw)
            press_h = self.press_alt(msg)
            self.handle_datapoint(
                msg, press_h,
                valid_magic=msg.magic == MAGIC
            )

    def handle_datapoint(self, msg, press_h, valid_magic=True, valid_checksum=True):
        if str(msg.latitude) != "-999.0":
            self.tempLAT = msg.latitude
            self.tempLON = msg.longitude
            self.tempALT = msg.altitude

        self.statusLabel.configure(text = "Connected", fg = 'green')

        for i in range(0, len(self.textboxes)):
            #sets mA to zero in anticpation of future implementation
            if self.dataLabel[i] == 'latitude' and str(msg.latitude) == "-999.0":
                self.textboxes[i].configure(text = str(self.tempLAT))
                continue
            if self.dataLabel[i] == 'altitude' and str(msg.altitude) == "-999.0":
                self.textboxes[i].configure(text = str(self.tempALT),)
                continue
            if self.dataLabel[i] == 'longitude' and str(msg.longitude) == "-999.0":
                self.textboxes[i].configure(text = str(self.tempLON))
                continue
            if self.dataLabel[i] == 'mA' :
                self.textboxes[i].configure(text = "0.0000000000")
                continue
            if self.dataLabel[i] == "pres_alt":
                self.textboxes[i].configure(text = press_h)
                continue
            if self.dataLabel[i] == 'magic':
                if valid_magic:
                    self.magicStatus.configure(text = "MAGIC: VALID", fg = 'green')
                    continue
                else:
                    self.magicStatus.configure(text = "MAGIC: INVALID", fg = 'red')
                    continue
            self.textboxes[i].configure(text = str(getattr(msg,self.dataLabel[i])), fg = '#39FF14')
        if not valid_checksum:
            self.checksumStatus.configure(text = "Checksum: INVALID", fg = 'red')
        else:
            self.checksumStatus.configure(text = "Checksum: VALID", fg = 'green')
        time.sleep(0.1)

        #self.scrolled_text.yview(tk.END)

    def close(self):
        print("Closed")
        self.flag = False
        self.statusLabel.configure( text = "disconnected", fg = 'red')
        self.radio.close()
        self.quit()
        self.f.close()


    def press_alt(self,data):
        gOxM = 0.284044 # (m*kg)/(s^2*mol)
        R = 8.3144598 # J/(mol*K)
        Tb = 273.15 #K
        hb = 0 #m
        Pb = 101325 #Pa
        #global initializing
        #global Pb
        #global Tb
        #if initializing > 0:
        #   temps.append(data.temp + 273.15)
        #   pressures.append(data.pressure)
        #   Tb = sum(temps) / len(temps)
        #   Pb = sum(pressures) / len(pressures)
        #   initializing -= 1
        if (22632.1 < data.pressure <= 101325):
            lapse = -0.0065
        elif (5474.89 <= data.pressure < 22632.1):
            lapse = 0
        elif (868.02 <= data.pressure < 5474.89):
            lapse = 0.001
        elif (110.91 <= data.pressure < 868.02):
            lapse = 0.0028
        else:
            lapse = 0
        if lapse != 0:
            h = hb + (Tb/lapse)*((math.pow((data.pressure/Pb),((-1*R*lapse)/gOxM))-1))
            #(((((math.log(data.pressure/Pb))/math.log((-1*gOxM)/(lapse*R)))-1)*Tb)/lapse + hb)
        elif lapse == 0:
            if data.pressure <= 0:
                h = 0
            else:
                h = (hb-R*Tb*math.log(data.pressure)/((gOxM)*math.log(Pb)))
        return h



if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(1100, 700)
    root.maxsize(1100, 700)
    TUI(root).pack(side="top", fill="both", expand=True)
    root.grid_columnconfigure(0, weight = 1)
    root.grid_columnconfigure(1, weight = 1)
    #root.bind('<Control-q>', self.quit)
    root.mainloop()
