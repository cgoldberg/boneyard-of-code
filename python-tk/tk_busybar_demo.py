#!/usr/bin/env python
# Python 3
# Corey Goldberg - 2009


import tkinter
from tkinter import ttk
import BusyBar


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('BusyBar Demo')
        ttk.Frame(self.root, width=200, height=100).pack()
        
        bb = BusyBar.BusyBar(self.root, width=150)
        bb.place(x=20, y=15)
        bb.on()
        self.root.update()
    

if __name__ == '__main__':
    root = tkinter.Tk()
    Application(root)
    root.mainloop()