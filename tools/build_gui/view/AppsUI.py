import os
import glob
import Tix
import ttk
import Tkinter, tkFileDialog
import AppsConfigUI
import targetUI
import AppsParam
import view 
import Tkinter as tk
from view import Configuration 
from view.Configuration import Configurer
from model import pathNamesConfig

class AppsUI(Tix.Frame):
    def __init__(self,parent,target):
        Tix.Frame.__init__(self,parent)
        self.parent=parent
        self.taregtInst=target
        self.instConfig=pathNamesConfig.PathAndNames(None)
        self.cpt=0
        self.initialize()
          
    def initialize (self):
        self.mesApps=[]
        self.i=0
        self.listeDesApplications=[]
        self.mymodel=[]
        self.sconsParamApps=":welcome"
        self.grid()
        self.pack(side=Tix.LEFT)
        self.b1=Tix.Button(self, text="add")
        self.b1.grid(row=2, column=1, sticky=Tix.W, padx=15, pady=2)
        b2=Tix.Button(self, text="delete", command=self.supprimer)
        b2.grid(row=2, column=2, sticky=Tix.W, padx=15, pady=2)
        self.b3=Tix.Button(self, text="config", command=self.configurer)
        self.b3.grid(row=2, column=3, sticky=Tix.W, padx=15, pady=2)  
        self.b3.configure(state=Tix.DISABLED)        
        self.tree = ttk.Treeview(self,columns=("", "source", "URL"),
            displaycolumns="URL")      
        self.tree.heading("#0", text="Source", anchor='w',)
        self.tree.heading("URL", text="URL", anchor='w',)
        self.tree.column("URL", stretch=1, width=300)
        self.tree.grid(column=0, row=0, sticky='nswe')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.listApps=[]
        self.tree.bind("<Button-1>", self.griser)

    def griser(self,event):
        self.b3.config(state=Tix.NORMAL)
            
    def setIp(self,newIp):
        self.url=newIp
        x = self.tree.get_children() 
        for item in x: 
            self.tree.delete(item)
        
        
        for a in self.listApps:
            self.cpt=self.cpt+1
            self.id=self.tree.insert('', 'end', text=a)
            u="http://%s/%s"% (self.url,a)
            self.tree.set(self.id, "URL",u)
        
        
    def getAppIp (self):
        return self.url
        
    def getAppsParams (self):
        self.tp=[]
        self.tp.append(["apps",self.sconsParamApps])
        return self.tp
    
    def supprimer (self):
        try:
            rows=self.tree.selection(selop=None, items=None)
            j=rows[0][3:]
            self.i=self.i-1
            s=int(j)
            v=self.mymodel[s-1-self.cpt]
            self.listApps.remove(v)
            if(len(self.listApps)==0):
                self.b3.configure(state=Tix.DISABLED)
            self.tree.delete(rows)
            
        except:
            pass
        
    def on_changed(self, selection):
        (model, iter) = selection.get_selected()
        return True
    
    def configurer(self):
        fenetre=tk.Toplevel()
        rows=self.tree.selection(selop=None, items=None);
        j=rows[0][3:]
        s=int(j)
        v=self.mymodel[s-1-self.cpt]
        app=view.Configuration.Configurer(fenetre,"apps",v)
        fenetre.title("Application Configuration")
      
   
    
            
        
        
