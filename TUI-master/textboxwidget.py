import tkinter as tk
import tkinter.scrolledtext as tkscrolled

class TextBox(tk.Frame):

    
    def __init__(self, parent, text, title):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.text = text
        self.title = title
        width, height = 10,20
        label = tk.Label(text = title)
        scrollText = tkscrolled.ScrolledText(10, width=width, height=height, wrap='word')
        scrollText.insert(1.0, self.text)
        label.pack()
        scrollText.pack()   
        
        
