
import Tix
import Tkinter as tk
import glob 
import os.path 
import Profil
import AppsUI
import AffichageIPV4
import AffichageIPV6
import tkMessageBox, tkFileDialog
import Image
import ImageTk



import string
from model.pathNamesConfig import PathAndNames
import model.targets as Targets
import view 


class targetUI(Tix.Frame):     
    def __init__(self,parent):
        Tix.Frame.__init__(self,parent)
        self.parent=parent
        self.initialize()

        
        


    def listdirectory(self,path): 
        fichier=[] 
        for filename in os.listdir(path):
            fichier.append( filename) 
         
        return fichier
       

        
    def initialize (self):
        self.grid()
        self.exist=False
        self.bool=False
        self.ok=False
        self.sconsParamTarget=[["ipaddr","192.168.1.2"],["target",""]]
        rootpath = PathAndNames.rootPath
        relatifpath= PathAndNames.target
        datapath = os.path.join(rootpath, relatifpath)
        self.listeDesTargets=self.listdirectory(datapath)
        self.varcombo = Tix.StringVar()
        self.leTarget=""
        self.frameIP=Tix.Frame(self, bd=2)

        text=Tix.Label(self.frameIP, text='ipaddr:')
        self.v = Tix.IntVar(value=False)
        self.b1 = Tix.Radiobutton(self.frameIP, text="IPV4",variable=self.v, value=1)
        self.b2 = Tix.Radiobutton(self.frameIP, text="IPV6",variable=self.v, value=2)
        self.b1.select()
        self.b1.grid(column=2, row=0, sticky='W')
        self.b2.grid(column=3, row=0, sticky='W')
        self.frameIP.grid(row=1,column=1,sticky='W')
        ipv4=Tix.Balloon()
        ipv4.bind_widget(self.b1, balloonmsg=" It defines IP addresses in a 32-bit format, \n which looks like 123.123.123.123. \nEach three-digit section can include a number from 0 to 255")
        ipv6=Tix.Balloon()
        ipv6.bind_widget(self.b2, balloonmsg="IPv6 uses 128-bit addresses,written in this format: \n hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh. \n Each hhhh section consists of a four-digit hexadecimal number")
        
       
        self.frameipv4=AffichageIPV4.AffichageIPV4(self.frameIP)
        text.grid(column=1, row=0,sticky='W')
         
        self.pack(fill=Tix.Y, expand=True, side=Tix.RIGHT)
        self.cpt=2
        self.r=3
        self.frameCombo=Tix.Frame(self, bd=2)
        self.frameTarget=Tix.Frame(self.frameCombo, bd=2)
        self.frameProfil=Tix.Frame(self.frameCombo, bd=2)
        self.var = Tix.StringVar()

        self.comboTarget = Tix.ComboBox(self.frameTarget, editable=1, dropdown=1, variable=self.var, command = self.Affiche)
        self.comboTarget.entry.config(state='readonly')
        self.recupererLesfichiersAvecProfil();
        self.removeNameFilesFromListTargets()

        self.cpt_target=0
        self.cpt_profil=0
        
        
#        self.comboTarget.pack(side=Tix.LEFT)
        self.comboTarget.grid(row=2, column=2)
        target=Tix.Label(self.frameTarget, text='target:')
#        target.pack(side=Tix.LEFT)
        target.grid(column=1, row=2,sticky='W')
        
#        self.comboTarget.pack(side=Tix.LEFT)
#        self.comboTarget.grid(row=2, column=2)
#        self.frameTarget.pack(side=Tix.LEFT)
        self.frameTarget.grid(row=2, column=2)
        
 #       self.frameProfil.pack(side=Tix.LEFT)
        self.frameProfil.grid(row=2, column=3)
        self.frameCombo.grid(row=2, column=1, sticky='W')
        self.lesProfils=[]
        self.tab=[]
        self.listeProfil=[]
        for h in self.listeDesFichiers:
            t=self.filterTargetsEtProfil(h)
            if not t in self.listeDesTargets:
                self.listeDesTargets.append(t)
            p=Profil.Profil(t)
            if not p.getName() in self.tab:
                self.tab.append(p.getName())
                self.lesProfils.append(p)
                p.setTab(self.listeProfil)
            else:
                p.setTab(self.listeProfil)

        for i in self.listeDesTargets:
            self.comboTarget.insert(self.cpt_target, i)
       
            
        self.frameDesc=Tix.Frame(self,width=300,height=300)
        self.textFrame = Tix.LabelFrame( self.frameDesc,label=' Target description' , padx=5, pady=5 ,bg='#dddddd' ,width=500,height=300)
        self.canvasFrameDescription=tk.Canvas(self.textFrame.frame,width=500,height=300, highlightthickness=0 )
        hbar=tk.Scrollbar(self.textFrame.frame,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=self.canvasFrameDescription.xview)
        vbar=tk.Scrollbar(self.textFrame.frame,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=self.canvasFrameDescription.yview)
        self.canvasFrameDescription.config(width=500,height=100)
        self.canvasFrameDescription.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvasFrameDescription.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.canvasFrameDescription.config(scrollregion=self.canvasFrameDescription.bbox('all'))
        self.canvasFrameDescription.create_text(250, 50, text='No description available ')
        self.frameDesc.grid(row=4, column=1)
        self.textFrame.pack()
        
        
        self.framePic=Tix.Frame(self, bd=2, padx=30)
        self.canvas=Tix.Canvas(self.framePic, width =140, height =140, bg='WhiteSmoke')
        self.canvas.create_text(70,70,text='No picture available') 
        self.canvas.grid(row=4, column=2)
        self.framePic.grid(row=4, column=2)
        
        frameBut=Tix.Frame(self, bd=2)
        self.run=Tix.Button(frameBut, text="config", command=self.config)
        self.run.grid(row=5, column=2, sticky='W',padx=0)
        frameBut.grid(row=5, column=1,sticky='W')
        self.run.configure(state=Tix.DISABLED)
        
        
    def validate(self):
        self.sconsParamTarget=[["ipaddr",""]]
        s=self.getIp()
        self.sconsParamTarget.append(["ipaddr",s])
        s=self.getTarget()
        self.sconsParamTarget.append(["target",s])
       
    def Affiche(self,evt):
        self.run.configure(state=Tix.NORMAL)
        valueTarget=self.var.get()
        self.bool=False
        targets = Targets.get()
        if valueTarget in targets:
            if len(targets[valueTarget]):
                self.comboProfil = Tix.ComboBox(self.frameProfil, editable=1, dropdown=1, variable=self.varcombo, command = self.AfficheValeur)
                self.profil=Tix.Label(self.frameProfil, text='profil:')
                self.profil.grid(column=6, row=2,sticky='W')
                self.comboProfil.entry.config(state='readonly')
                self.comboProfil.grid(row=2, column=7)
                self.bool=True
                self.ok=True
                for i in targets[valueTarget]:
                    self.comboProfil.insert(0, i)
                
#         for p in self.lesProfils:
#             if p.getName()== valueTarget:
#                     self.comboProfil = Tix.ComboBox(self.frameProfil, editable=1, dropdown=1, variable=self.varcombo, command = self.AfficheValeur)
#                     self.profil=Tix.Label(self.frameProfil, text='profil:')
#                     self.profil.grid(column=6, row=2,sticky='W')
#                     self.comboProfil.entry.config(state='readonly')
# #                    self.comboProfil.pack(side=Tix.LEFT)
#                     self.comboProfil.grid(row=2, column=7)
#                     self.bool=True
#                     self.ok=True
#                     for i in p.getProfils():
#                         self.comboProfil.insert(0, i)
                    
        if self.bool==False:
            self.frameProfil.destroy()
            self.frameProfil=Tix.Frame(self.frameCombo, bd=2)
 #           self.frameProfil.pack(side=Tix.LEFT)
            self.frameProfil.grid(row=2, column=3)
            self.ok=False
        
        if self.ok== False :
            self.t=self.var.get()
            self.leTarget=self.t
            self.displayTargetDescription(self.leTarget)
            self.displayTargetPicture(self.leTarget)
            
   
        
   
   
    def config(self):
        fenetre=tk.Toplevel()
        self.targetpath=PathAndNames.target+"/"+self.leTarget
        view.Configuration.Configurer(fenetre,self.targetpath,None)
        """fenetre.geometry('400x300')
        fenetre.resizable(width=False, height=False)"""

    
    def destroyIPV4(self):
        self.frameipv4.destroy()
        
    def destroyIPV6(self):
        self.frameipv6.destroy()
        
    def OnCheckBoxClick(self):
        iTemp = self.enabled.get()

    
    def recupererLesfichiersAvecProfil(self):
        self.listeDesFichiers=[] 
        for i in self.listeDesTargets:
            if  "_" in i:
                self.listeDesFichiers.append(i)
                
                
    
    def removeNameFilesFromListTargets(self):
        for i in self.listeDesFichiers:
                self.listeDesTargets.remove(i)
                
                
    def filterTargetsEtProfil(self,j):
        i=j.find("_")
        t=j[0:i]
        profil=j[i+1:]
        if not t in self.listeDesTargets:
            self.listeProfil=[]
        return t
    
    def getIp (self):
        s=""
        if self.v.get()==1 :
            
            s=self.frameipv4.getIpValue()
        else :
            s= self.frameipv6.getIpVAlue()
        return s
        
    def AfficheValeur (self,evt):
        self.leTarget= self.var.get()
        trouve=False
        i=0
        while trouve==False :
            p =self.lesProfils[i]
            if p.getName()== self.var.get():
                    trouve=True
                    
                    self.leTarget+="_"
                    self.leTarget+=self.varcombo.get()
            else : i=i+1
        self.displayTargetDescription(self.leTarget)
        self.displayTargetPicture(self.leTarget)  
        
    def getTarget (self):
        return self.leTarget
    
         
    def getTargetParams (self):
        return self.sconsParamTarget
        
    def setTargetIpParams(self,ip):
        self.sconsParamTarget[0][1]=ip
        
    def setTargetTarParams(self,target):
        self.sconsParamTarget[1][1]=target
    
     
    def displayTargetPicture(self,targetname):
        try:
            rootpath = PathAndNames.rootPath 
            datapath = os.path.join(rootpath,PathAndNames.target,targetname,PathAndNames.image)
            
            
            im = Image.open(datapath) 
            data = list(im.getdata())
            imNew=Image.new(im.mode ,im.size) 
            imNew.putdata(data)
            self.photo = ImageTk.PhotoImage(imNew)
            self.canvas.delete(tk.ALL)
            self.canvas.create_image(70,70,image=self.photo)
            self.canvas.image = self.photo 
            self.canvas.grid(row=4, column=2)
            self.framePic.grid(row=4, column=2)
        except(IOError):
            self.canvas.delete(tk.ALL)
            self.canvas.create_text(70,70,text='No picture available') 
              
    def displayTargetDescription(self,targetname): 
        try:   
            rootpath = PathAndNames.rootPath 
            datapath = os.path.join(rootpath,PathAndNames.target,targetname,PathAndNames.description)
            source = open(datapath, "r")
            toutesleslignes = source.readlines()
            self.canvasFrameDescription.delete(tk.ALL)  
            self.k=1
            for i in toutesleslignes:
                if i!=" ":
                    self.canvasFrameDescription.create_text(1, self.k*20, text=i, anchor=Tix.W )
                    self.k=self.k+1
            self.canvasFrameDescription.config(scrollregion=self.canvasFrameDescription.bbox('all'))
        except(IOError):
            self.canvasFrameDescription.delete(tk.ALL)
            self.canvasFrameDescription.config(scrollregion=self.canvasFrameDescription.bbox('all'))
            self.canvasFrameDescription.create_text(250, 50, text='No description available ') 
            
            
            
