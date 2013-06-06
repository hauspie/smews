import glob 
import os.path 
import AppsConfig
import ttk
import Tkinter, tkFileDialog
class SearchArgs:
    def __init__(self,parent):
        baliseOuverte = "<args>" 
        balisefermante = "</args>"
        self.path="/home/rubi/Desktop/m1_s2/smews-master/apps/calendar"
        self.list=self.listdirectory(self.path)
        self.lesArgs=[]
        self.lesApps=[]
        cpt=0
        for i in self.list:
            self.fichier = open(i,"r")
            self.oneline = self.fichier.readline()
            while self.oneline:
                if baliseOuverte in self.oneline:
                    self.oneline = self.fichier.readline()
                    while not balisefermante  in self.oneline:
                        self.lesArgs=self.decouperArgs(self.oneline)
                        self.tab=self.lesArgs[1:len(self.lesArgs)-1]
                        self.appConf= AppsConfig.AppsConfig(self.decouperNameAppli(self.path))
                        for j in self.tab:
                            value=self.decouperLaValeur(j)
                            self.appConf.getArgs().append(value)
                            self.appConf.setArgs(self.appConf.getArgs())
                        self.lesApps.append(self.appConf)
                        self.oneline = self.fichier.readline()
                    
                self.oneline = self.fichier.readline()
            self.fichier.close() 
            
                
        
    def listdirectory(self,path): 
        fichier=[] 
        for root, dirs, files in os.walk(path): 
            for i in files: 
                fichier.append(os.path.join(root, i)) 
        return fichier

    def decouperNameAppli(self,application):
        app=os.path.basename(application)
        return app
        
    def decouperArgs (self, args):
        lesArgs=args.split()
        return lesArgs
        
    def decouperLaValeur(self,value):
        i=value.find("=")
        t=value[i+1:]
        v=value[0:i]
        couple=AppsConfig.NomValeur(v,t)
        return couple 
    
    def getAppsArgs(self,nameApps):
        "for i in self.lesApps:"
        bool=False
        tab=[]
        cpt=0
       
        while not bool:
            i=self.lesApps[cpt]
            if i!=nameApps:
                cpt=cpt+1
            else :
                bool=True
        cpt=0
        if bool:
            i=self.lesApps[cpt+1:][cpt]
            while(i==nameApps):
                tab.append(i.getArgs())
                cpt=cpt+1
                i=self.lesApps[cpt+1:][cpt]
        return tab
            
             
             
         

  
