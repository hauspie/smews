from view.interface import interface 
from model.model import Model
import Tkinter, tkFileDialog
import view
import Tix
import subprocess
from model import pathNamesConfig


from subprocess import Popen, PIPE
from getpass import getpass
from os import chdir
import os
import tkMessageBox, tkFileDialog

class Controleur:
    def __init__(self, root):
        self.model = Model()
        self.model.myModel.addCallback(self.ipChanged)
        self.instConfig=pathNamesConfig.PathAndNames(None)
        self.interface=interface(root)
        self.interface.f1.b1.config(command=self.affichageIPV4)
        self.interface.f1.b2.config(command=self.affichageIPV6)
        self.interface.f2.b1.config(command=self.ajouter)
        self.interface.build.config(command=self.build)
        self.interface.up.config(command=self.upload)
        self.interface.kill.config(command=self.kill)
        self.interface.f1.frameipv4.E4.bind("<Return>",self.OnPressEnter)

        self.ipChanged(self.model.myModel.get())
        self.interface.f1.b1.config(command=self.affichageIPV4)
        self.interface.f1.b2.config(command=self.affichageIPV6)
        self.interface.title("Compile")
        self.interface.mainloop()
        
    
    def affichageIPV4(self):
        self.interface.f1.frameipv4=view.AffichageIPV4.AffichageIPV4(self.interface.f1.frameIP)
        if self.interface.f1.exist:
            self.interface.f1.destroyIPV4()
            self.interface.f1.exist=False;
        self.interface.f1.destroyIPV6()
        self.interface.f1.frameipv4=view.AffichageIPV4.AffichageIPV4(self.interface.f1.frameIP)
        self.interface.f1.frameipv4.E4.bind("<Return>",self.OnPressEnter)
        
    def affichageIPV6(self):
        self.interface.f1.destroyIPV4()
        self.interface.f1.frameipv6=view.AffichageIPV6.AffichageIPV6(self.interface.f1.frameIP)
        self.interface.f1.exist=True
        
    def OnPressEnter(self,event):  
       
        if self.interface.f1.frameipv4.focus_get()==self.interface.f1.frameipv4.E4:
            if self.interface.f1.frameipv4.OnValidate(self.interface.f1.frameipv4.E4):
                
                self.ok= Tix.Label(self.interface.f1.frameipv4.f,text="ok")
                self.ok.grid(row=2, column=7)
                self.interface.f1.frameipv4.f.grid(row=2,column=7)
                self.interface.f1.frameipv4.getIpValue()
                self.interface.f1.frameipv4.booleanOk=True
                self.interface.f1.frameipv4.E4.configure(bg='white')
           


            else :
                tkMessageBox.showwarning("error","please enter a number between 0 and 255")
                b=Tix.Balloon()
                b.bind_widget(self.interface.f1.frameipv4.E1, balloonmsg="please enter a number between 0 and 255")
                self.interface.f1.frameipv4.E4.focus_set()
                self.interface.f1.frameipv4.E4.selection_range(0, Tix.END)
                self.interface.f1.frameipv4.error=True

            if self.interface.f1.frameipv4.OnValidate(self.interface.f1.frameipv4.E4):
                self.model.addTargetParams(self.interface.f1.getIp())
                self.interface.f1.setTargetIpParams(self.interface.f1.getIp())
            if (self.interface.f1.frameipv4.error==True) :
                for w in self.interface.f1.frameipv4.f.winfo_children():
                    w.destroy()
                self.interface.f1.frameipv4.error=False
                
    def validateTargetParam(self):
        s=self.interface.f1.getTarget()
        self.interface.f1.setTargetTarParams(s)
        self.optionParams=[]
        for i in self.interface.f3.options:
            v=i[1].get()
            if ((v=="1")):
                if (i[0]=="endian"):
                    self.interface.f3.optionParams.append([i[0],"big"])
                else:
                    self.interface.f3.optionParams.append([i[0],"false"])

        dis=""
        for i in self.interface.f3.disable: 
            v=i[1].get()
            if (v=="1"):
                if(dis==""):
                    dis=dis+i[0]
                else:
                    dis=dis+","+i[0]
        self.interface.f3.optionParams.append(["disable",dis])
        self.interface.cmdLine()

       
    
    def ipChanged(self, newIp):
        self.interface.f2.setIp(newIp)
        
    def ajouter(self):

        rootpath =self.instConfig.rootPath     
        self.datapath = os.path.join(rootpath, "apps/")
       

        dirname = tkFileDialog.askdirectory(initialdir=self.datapath,title='Please select a directory')  
        self.app=os.path.basename(dirname)
    
        if len(dirname ) > 0:
            appParam=view.AppsParam.AppsParam(self.app,"http://192.168.1.4/%s"%self.app)
            id=self.interface.f2.tree.insert('', 'end', text=self.app)
            self.url=""
            self.index=id
            self.url=self.model.myModel.get()
            self.u="http://%s/%s/%s"% (self.url,self.app,"index.html")
            self.interface.f2.tree.set(id, "URL",self.u)
            "self.interface.f2.mymodel.insert( self.interface.f2.i,self.app)"
            self.interface.f2.mymodel.append( self.app)
            self.interface.f2.listApps.append(self.app)
           
            
        self.interface.f2.i=self.interface.f2.i+1
        while ("" in self.interface.f2.listApps):
            self.interface.f2.listApps.remove("")
        self.interface.f2.sconsParamApps=""
        self.interface.f2.mesApps=[]
#        self.interface.f2.sconsParamApps= self.interface.f2.sconsParamApps +":welcome"
       
     

    ##************************fonction qui compile***********************## 
    def build(self):
        for a in self.interface.f2.listApps:
            
            if (self.interface.f2.sconsParamApps==""):
                self.interface.f2.sconsParamApps= self.interface.f2.sconsParamApps+"," +a
            else:
                self.interface.f2.sconsParamApps= self.interface.f2.sconsParamApps+"," +a
            self.interface.f2.mesApps.append(a)
        
        self.validateTargetParam()
        command="scons "+self.interface.cmd #linux
        
        chdir(self.instConfig.rootPath)
        ret = os.system(command)
        if ret != 0:
            tkMessageBox.showwarning("error", "Failed to build: {0} returned {1}".format(command, ret))
            return False
        return True
        
    ##************************fonction qui execute***********************##    
    def upload (self):
        if not self.build():
            return False
        if not self.kill():
            return False
        rootpath =self.instConfig.rootPath     
        relatifpath= self.instConfig.target
        datapath = os.path.join(rootpath, relatifpath)
        path= os.path.join(datapath,self.interface.f1.getTarget())
        cmd = self.instConfig.run_script + " -gui"
        command = os.path.join(path, cmd)
        ret = os.system(command)
        if ret != 0:
            tkMessageBox.showwarning("error", "Failed to program: {0} returned {1}".format(command, ret))
            return False
        return True

    def kill(self):
        rootpath =self.instConfig.rootPath     
        relatifpath= self.instConfig.target
        datapath = os.path.join(rootpath, relatifpath)
        path= os.path.join(datapath,self.interface.f1.getTarget())
        cmd = self.instConfig.kill_script + " -gui"
        command = os.path.join(path, cmd)
        ret = os.system(command)
        if ret != 0:
            tkMessageBox.showwarning("error", "Failed to kill: {0} returned {1}".format(command, ret))
            return False
        return True
        

