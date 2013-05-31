import Tkinter, tkFileDialog
import tkMessageBox, tkFileDialog
import Tix
import os
from subprocess import call
from getpass import getpass


from model.model import Model
from model import pathNamesConfig
from view.interface import interface



class Controleur:
    def __init__(self, root):
        self.model = Model()
        self.model.myModel.addCallback(self.ipChanged)
        self.instConfig=pathNamesConfig.PathAndNames(None)
        self.interface = interface(root)
        self.interface.f1.b1.config(command=self.affichageIPV4)
        self.interface.f1.b2.config(command=self.affichageIPV6)
        self.interface.f2.b1.config(command=self.ajouter)
        self.interface.build.config(command=self.build)
        self.interface.up.config(command=self.upload)
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
                print self.interface.f1.getIp()
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
            print v
            if ((v=="1")):
                if (i[0]=="endian"):
                    self.interface.f3.optionParams.append([i[0],"big"])
                else:
                    self.interface.f3.optionParams.append([i[0],"false"])

        dis=""
        for i in self.interface.f3.disable: 
            v=i[1].get()
            print v
            if (v=="1"):
                if(dis==""):
                    dis=dis+i[0]
                else:
                    dis=dis+","+i[0]
        self.interface.f3.optionParams.append(["disable",dis])
        print self.interface.f3.optionParams
        self.interface.cmdLine()

       
    
    def ipChanged(self, newIp):
        self.interface.f2.setIp(newIp)
        
    def ajouter(self):

        rootpath =self.instConfig.rootPath     
        self.datapath = os.path.join(rootpath, "apps/")
       

        dirname = tkFileDialog.askdirectory(initialdir=self.datapath,title='Please select a directory')  
        self.app=os.path.basename(dirname)
    
        if len(dirname ) > 0:
            print "You chose %s" % self.app
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
            print "modeCTRL=" , self.interface.f2.mymodel
           
            
        self.interface.f2.i=self.interface.f2.i+1
        while ("" in self.interface.f2.listApps):
            self.interface.f2.listApps.remove("")
        self.interface.f2.sconsParamApps=""
        self.interface.f2.mesApps=[]
        self.interface.f2.sconsParamApps= self.interface.f2.sconsParamApps +":welcome"
        print "slistapps",self.interface.f2.listApps
       
     

    ##************************fonction qui compile***********************## 
    def build(self):
        for a in self.interface.f2.listApps:
            
            if (self.interface.f2.sconsParamApps==""):
                self.interface.f2.sconsParamApps= self.interface.f2.sconsParamApps+"," +a
            else:
                self.interface.f2.sconsParamApps= self.interface.f2.sconsParamApps+"," +a
            self.interface.f2.mesApps.append(a)
        
        self.validateTargetParam()
        """command="C:\Python27\Scripts\scons "+self.interface.cmd""" #windows
        command="scons "+self.interface.cmd #linux
        
        print command     
        rootpath = "../../../../../.."
        relatifpath= 'smews-master'
        fn = os.path.join(os.path.dirname(__file__), rootpath)
        print fn
        path=fn
        os.chdir(path) 
        
        call('echo |%s' % command,shell=True)
        self.interface.up.configure(state=Tix.NORMAL)
    ##************************fonction qui execute***********************##    
    def upload (self):
        rootpath = "../../../../../.."
        relatifpath= 'targets'
        fn = os.path.join(os.path.dirname(__file__), rootpath)
        datapath = os.path.join(fn, relatifpath)
        path= os.path.join(datapath,self.interface.f1.getTarget())
        os.chdir(path)
        command="./run.sh &"
        path="chmod +x run.sh"
        os.system('echo | %s' % path)
        self.interface.quit()
        os.system('echo |gksudo -w  %s' % command)
        

