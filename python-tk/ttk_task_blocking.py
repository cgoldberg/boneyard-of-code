#!/usr/bin/env python
# Python 3
# Corey Goldberg - 2009


import tkinter
from tkinter import ttk
import urllib.request



class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('Blocking Command Demo')
        
        self.init_widgets()
            
            
    def init_widgets(self):
        self.btn = ttk.Button(self.root, command=self.get_url, text='Get Url', width=8)
        self.btn.grid(column=0, row=0, sticky='w')
        
        self.entry = ttk.Entry(self.root, width=60)
        self.entry.grid(column=0, row=0, sticky='e')
        
        self.txt = tkinter.Text(self.root, width=80, height=20)
        self.txt.grid(column=0, row=1, sticky='nwes')
        sb = ttk.Scrollbar(command=self.txt.yview, orient='vertical')
        sb.grid(column=1, row=1, sticky='ns')
        self.txt['yscrollcommand'] = sb.set
        

    def get_url(self):
        url = self.entry.get()
        headers = urllib.request.urlopen(url).info()
        self.txt.insert(tkinter.INSERT, headers)
    
    

if __name__ == '__main__':
    root = tkinter.Tk()
    Application(root)
    root.mainloop()
