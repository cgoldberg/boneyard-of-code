#!/usr/bin/env python
# Python 3
# Corey Goldberg - 2009


import tkinter
from tkinter import ttk

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('Hello World')
        ttk.Frame(self.root, width=200, height=100).pack()
        ttk.Label(self.root, text='Hello World').place(x=10, y=10)

if __name__ == '__main__':
    root = tkinter.Tk()
    Application(root)
    root.mainloop()