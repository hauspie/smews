import glob 
import os.path 
import AppsConfig
import ttk
import Tkinter, tkFileDialog
import Config
import Tix


class AppsConfigUI (Tix.Tk):
    def __init__(self,parent,nameApps):
        self.args=Config.SearchArgs(None).getAppsArgs(nameApps)
        Tix.Tk.__init__(self,parent)
        self.parent=parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        self.pack(side=Tix.LEFT)
        self.frame=Tix.Frame(self, bd=2)
        cptCol=0
        cptLigne=0
        for j in self.args:
            tabElements=j.getArgs()
            for a in tabElements:
                if (a.getName()=="name"):
                    value=a.getValue()
                    self.text=Tix.Label(self.frame, text=value+':')
                    self.text.grid(column=cptCol, row=cptLigne,sticky='W')
                    cptCol=cptCol+1
                    self.valeur = Tix.StringVar()
                    self.entry= Tix.Entry(self.frame,textvariable=self.valeur)
                    self.entry.pack(padx=2,side=Tix.LEFT)
                    self.entry.grid(column=cptCol, row=cptLigne, sticky='W')
                    self.frame.grid(row=cptLigne, column=1)
                    self.grid(row=1, column=2,sticky='W')
                if (a.getName()=="type"):
                    self.entry.configure(validate="focus",validatecommand=self.validateType(self.entry,a.getValue()))
                if (a.getName()=="size"):
                    self.entry.configure(width=a.getValue())
                    
            cptLigne=cptLigne+1
                
    def validateType(self,entry,type):
        if entry.get().dtype==type:
            return entry.get()
        else:
            return None
            
        
                    
        
    
