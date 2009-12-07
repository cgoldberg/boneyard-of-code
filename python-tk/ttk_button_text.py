#!/usr/bin/env python
# Python 3
# Corey Goldberg - 2009


import tkinter
from tkinter import ttk


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('Button Demo')
        ttk.Frame(self.root, width=250, height=100).pack()
        
        self.init_widgets()
            
    def init_widgets(self):
        ttk.Button(self.root, command=self.insert_txt, text='Click Me', width='10').place(x=10, y=10)
        self.txt = tkinter.Text(self.root, width='15', height='2')
        self.txt.place(x=10, y=50)
        
    def insert_txt(self):
        self.txt.insert(tkinter.INSERT, 'Hello World\n')


if __name__ == '__main__':
    root = tkinter.Tk()
    Application(root)
    root.mainloop()