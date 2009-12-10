#!/usr/bin/env python
# Python 3
# Corey Goldberg - 2009


from threading import Thread
import urllib.request
import time 
import tkinter
from tkinter import ttk
import BusyBar



class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('Non-Blocking Task Demo')
        
        self.init_widgets()
            
            
    def init_widgets(self):
        self.btn = ttk.Button(self.root, command=self.get_url, text='Run Task', width=12)
        self.btn.grid(column=0, row=0, sticky='w')

        self.txt = tkinter.Text(self.root, width=40, height=10)
        self.txt.grid(column=0, row=1, sticky='nwes')
        sb = ttk.Scrollbar(command=self.txt.yview, orient='vertical')
        sb.grid(column=1, row=1, sticky='ns')
        self.txt['yscrollcommand'] = sb.set
        
        
    def get_url(self):
        self.btn.configure(state=tkinter.DISABLED)
        
        bb = BusyBar.BusyBar(self.root, width=150)
        bb.place(x=60, y=40)
        bb.on()
        self.root.update()
        
        t = Task()
        t.start()
        
        while t.is_alive():
            self.root.update()
            self.txt.insert(tkinter.INSERT, 'Waiting\n')
            self.txt.see(tkinter.END)
            time.sleep(0.1)
            
        bb.destroy()
        self.btn.configure(state=tkinter.NORMAL)
        
        self.txt.insert(tkinter.INSERT, 'Finished\n')
        self.txt.see(tkinter.END)



class Task(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        # do some real work here
        time.sleep(3)
        
        
        
if __name__ == '__main__':
    root = tkinter.Tk()
    Application(root)
    root.mainloop()
