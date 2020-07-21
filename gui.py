# -*- coding: utf-8 -*-
# @Author: de retour
# @Date:   2019-11-02 05:23:41
# @Last Modified by:   de retour
# @Last Modified time: 2019-12-31 18:50:34
from tkinter import *

class App():
    def __init__(self):
        self.instance = Tk() 
        self.instance.wm_attributes('-topmost',1)    #窗口置顶               


    def button(self, text, callback):
        btn = Button(self.instance, text = text, command = callback)
        btn.pack()

    def text(self, width=100, height=100):
        text = Text(self.instance, width=width, height=height)
        text.pack()

    def label(self, text, **props): # text, bg, width, height, wraplength, justify
        tk_label = Label(self.instance, text = text, **props)
        tk_label.pack()

    def menu(self, items):
        tk_list = Listbox(self.instance)
        for i, item in enumerate(items):
            tk_list.insert(i, item)
        tk_list.pack()
        return tk_list

    def input(self, callback): 
        tk_input = Entry(self.instance)
        # tk_input.place(height=300, width=100)
        tk_input.bind('<Return>', callback)
        tk_input.pack()  #side = LEFT
        return tk_input

    def set_title(self, title):
        self.instance.title(title)
        return self

    def set_size(self, width, height):
        self.instance.geometry("%sx%s" % (width, height))
        return self

    def set_loc(self, x, y):
        self.instance.geometry("+%s+%s" % (x, y))
        return self
    
    def run(self):
        self.instance.mainloop() 


