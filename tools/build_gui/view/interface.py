import Tix
from Tkinter import *
import targetUI
import glob 
import os.path 
import AppsUI
import options
import subprocess
from subprocess import Popen, PIPE
from getpass import getpass
from os import chdir
import sys
import time
import model
import view 
from model.model import Model

class interface(Tix.Tk):     
    def __init__(self,parent):
        Tix.Tk.__init__(self,parent)
        self.parent=parent
        self.initialize()


    def listdirectory(self,path): 
        fichier=[] 
        l = glob.glob(path+'\\*') 
        for filename in os.listdir(path):
            fichier.append( filename) 
         
        return fichier
    def initialize (self):
        self.grid()
        self.framePrincipale=Tix.Frame(self ,bd=2,relief= GROOVE)

        nb = Tix.NoteBook(self.framePrincipale)
        nb.add("page1", label="Target")
        nb.add("page3", label="Options")

        nb.add("page2", label="Applis")
        self.cmd=""
        p1 = nb.subwidget_list["page1"]
        p2 = nb.subwidget_list["page2"]
        p3 = nb.subwidget_list["page3"]
        self.f1=view.targetUI.targetUI(p1)
        fra1=self.f1
        fra1.grid(sticky='EW')
        fra1.pack(side=Tix.LEFT)
        self.f2=view.AppsUI.AppsUI(p2,self.f1)
        fra2=self.f2
        fra2.grid(sticky='EW')
        fra2.pack(side=Tix.LEFT)
        self.f3=view.options.OptionsUI(p3)
        fra3 = self.f3
        fra3.grid(sticky='EW')
        fra3.pack(side=Tix.LEFT)
        
        nb.pack(fill=Tix.BOTH, padx=5, pady=5,side=TOP, anchor=W, expand=YES)
        nb.grid(row=0, column=0,sticky='W')
               
        self.framePrincipale.pack(fill=Tix.BOTH, padx=5, pady=15,side=TOP, anchor=W, expand=YES)
        self.framePrincipale.grid(row=0, column=0,sticky='W')
        
        frame=Tix.Frame(self, bd=2)
        self.build=Tix.Button(frame, text="build",font=("Helvetica", 12))
        self.build.grid(row=4, column=0, sticky='W')
        self.up=Tix.Button(frame,state=DISABLED, text="upload", font=("Helvetica", 12))
        self.up.grid(row=4, column=1, sticky='W', padx=5, pady=5)
        
        frame.pack(fill=Tix.BOTH,  side=TOP, anchor=W, expand=YES)
        frame.grid(row=4, column=0,sticky='W', padx=5, pady=5)
        self.geometry('770x400')

    def cmdLine(self):
        self.lesParams=[]
        self.cmd=""
        self.lesParams.append(self.f1.getTargetParams())
        
        self.lesParams.append(self.f2.getAppsParams())
        self.lesParams.append(self.f3.getOptionsParam())
        for c in self.lesParams:
            for i in c :                    
                for j in i[1:] :
                    if(not(j=='')):
                        
                        self.cmd=self.cmd+i[0]+"="
                        self.cmd=self.cmd+j+" "
                        
    

        
    def ipChanged(self, ip):
        self.f2.setIp(self.f1.getIp())
        
    def targetChanged(self, target):
        self.f1.setTargetTarParams(target)
        
    def appChanged(self, app):
        self.f2.setAppsParams(app)
        
