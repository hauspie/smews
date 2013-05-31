import os
import glob
import ttk
import Tkinter, tkFileDialog
import tkMessageBox, tkFileDialog
from Tkinter import *
import Tix
class AffichageIPV6(Tix.Frame):
    def __init__(self,frameIP):
        Tix.Frame.__init__(self,frameIP)
        self.fip=frameIP
        self.initialize()
        
        
    def initialize (self):
        self.grid()
        frame=Tix.Frame(self, bd=2)
        self.valeur = Tix.StringVar()
        self.entry= Tix.Entry(frame,textvariable=self.valeur)
        self.entry.pack(padx=2,side=Tix.LEFT)
    
        self.entry.grid(column=2, row=1, sticky='W')
        frame.grid(row=2, column=1)
        self.grid(row=2, column=2,sticky='W')


    def getIpVAlue(self):
        return self.entry.get()