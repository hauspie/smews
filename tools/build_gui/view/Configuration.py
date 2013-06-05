import glob 
import os.path 
import AppsConfig
import  tkFileDialog
from controleur import SimpleParser 
from Tix import *
import view 
import fileinput
import tkMessageBox, tkFileDialog
from model import pathNamesConfig

class Configurer(Frame) :
    def __init__(self,parent,pathparam,tabApps):
        Frame.__init__(self,parent)
        self.instConfig=pathNamesConfig.PathAndNames(None)

        self.exist=False
        self.parent=parent
        self.p=SimpleParser.Parser()
        self.liste=[]
        self.listFiles=[]
        rootpath = self.instConfig.rootPath
        self.src=pathparam
        if (pathparam==self.instConfig.apps):
            
            self.pathconfig=pathparam
            self.datapath = os.path.join(rootpath, self.pathconfig,tabApps)
            self.listAppFile=self.p.listdirectory(self.datapath)
            for j in self.listAppFile:
                self.listFiles.append(j) 
        else:
            self.pathconfig=pathparam
            self.datapath = os.path.join(rootpath, self.pathconfig)
            print self.datapath
            self.listFiles=self.p.listdirectory(self.datapath)
            
        self.allLists=[]
        self.row=0
        self.column=0
        self.tk.eval('package require Tix')
        
        self.ScrolledCanvas=Canvas(self,width=250,height=250, highlightthickness=0)
       
        self.frameLabelFrames=Frame(self)
        self.frameLabelFrames.pack()
         
       
            
        self.initialize()
    

    def initialize(self):
        self.grid()
        cptInsert=0
        self.listOfFiles=[]
        self.valTot=[]
        self.namesTot=[]
        self.nameWidgets=[]
        
        for li in self.listFiles:
            self.list=self.p.extractPropsFromXml(li)
            n=0
            for label in self.p.getLabelGroup():
                if(len(self.p.getLabelGroup())>1):
                
                    l=self.p.getValues()
                    l1=self.p.getKeys()
                    print "l",l,li
                    print "l1",l1
                    print "aa",self.p.getLesCles()[1]
                    print "aa",self.p.getLesVals()[1]
                    print "ppp",self.p.getTab()

                self.f=LabelFrame( self.frameLabelFrames,bg='#eeeeee',label=label,labelside=ACROSSTOP, padx=5, pady=5 )
                self.frame=Frame(self.f, bd=2)
                self.frame=self.f.frame
                
                self.frame2=Frame(self.frame, bd=2)
                cpt=0
                self.listeName=[]
                self.listeWid=[]
                self.val=[]
                self.c=0
                self.index=0
                bool=False;
                bool2=False;
                self.value=StringVar()
                self.varButton=[]

                if(len(self.list)>0):
                    self.exist=True
                "for i in range(len(self.list)):"


                for i in range(len(self.p.getTab()[n])):


                    """self.keys=self.p.getKeys()[cpt]
                    self.values=self.p.getValues()[cpt]"""
                    if(len(self.p.getLabelGroup())>1):

                        self.keys=self.p.getLesCles()[n][cpt]
                        self.values=self.p.getLesVals()[n][cpt]
                        print "mmmmmmmmmmmmmmmmmm",self.values
                        print "nnnnnnnn",self.keys

                    else:
                        self.keys=self.p.getKeys()[cpt]
                        self.values=self.p.getValues()[cpt]
                        

                    k=0
                    while(k<(len(self.keys))):  
                            
                        if (self.values[0][0]=='arg') and not(self.values[1][0]=="Checkbutton") and not (self.values[1][0]=="Radiobutton")  :  
                            if (bool2==False):
                                self.row+=1
        
                            bool2=True
                            self.column=0
                            if (self.keys[k]=='name'):
                                self.column=0;
                                self.name=self.values[1][k]
                                self.label(self.name)
                                self.listeName.append(self.name)
                            elif (self.keys[k]=='show'):
                                self.column+=1;
                                self.c=self.c+1
                                data=self.values[1][k]
                                print data
                                self.wid=self.show(data)
                                self.listeWid.append(data)
    
                            elif (self.keys[k]=='Value'):
                                valeur = StringVar()
                            elif (self.keys[k]=='to'):
                                self.wid.config(to=self.values[1][k])
                            elif (self.keys[k]=='from'):
                                self.wid.config(from_=self.values[1][k]) 
                            elif (self.keys[k]=='orient'):
                                self.wid.config(orient=self.values[1][k]) 
                            elif (self.keys[k]== "resolution"):
                                self.wid.config(resolution=self.values[1][k]) 
                            elif (self.keys[k]== "tickinterval"):
                                self.wid.config(tickinterval=self.values[1][k])
                            elif (self.keys[k]== "length"):
                                self.wid.config(length=self.values[1][k])
                        if (self.values[0][0]=='select'):
                            pass
                        if (self.keys[k]=='state'):
                                self.wid.entry.config(state=self.values[1][k])
                        elif (self.values[0][0]=='option'):
                            if (self.keys[k]=='Value'):
                                print "oooooooooooooooooooooooooooo",self.values[1][k]
                                self.wid.insert(END,self.values[1][k])
                            """if (self.keys[k]=='selected'):
                                self.val[-1].set(self.values[1][k+1])"""
        
                        elif (self.values[0][0]=='arg') and ((self.values[1][0]=="Checkbutton") or (self.values[1][0]=="Radiobutton")  ) :
                            self.frame2=Frame(self.frame, bd=2)
                            self.value=StringVar()
                            bool=True;
                            self.column=0
                            self.row+=1
                            data=""
                        if (self.keys[k]=='name'):
                                self.column=0
                                name=self.values[1][k]
                                self.label(name)
                                self.listeName.append(name)
                                
                        if (self.values[0][0]=='input'):
        
                            if (self.keys[k]=='show'):
                                self.c=self.c+1
                                self.column+=1;
                                data=self.values[1][k]
                                print data
                                bool=True;
                                self.wid=self.show(data)
                                self.listeWid.append(data)
                                if(not(self.value in self.varButton)):
                                    self.varButton.append(self.value)
                                    self.val.append(self.value)
                                    self.nameWidgets.append(data)
        
                            if (self.keys[k]=='Value'):
                                valeur = StringVar()
                                self.wid.config(variable=self.value)
                                if (data=="Checkbutton"):
                                    self.wid.config(onvalue=self.values[1][k])
                                else:
                                    self.wid.config(value=self.values[1][k])
                                print self.values[1][k]
                                def wid():
                                    pass
                                self.wid.config(command=wid)
                            if (self.keys[k]=='text'):
                                
                                name=self.values[1][k]
                                self.wid.config(text=name)
                                
                            if (self.keys[k]=='selected'):
                                self.wid.select()
                            else:
                                self.wid.deselect()
                        
                            
                        k=k+1
                    cpt=cpt+1
                    
                    if (bool2==True): 
                        self.row+=1
                        self.column=0
                        bool2=False
                    else :
                        
                        self.frame2.pack(fill=BOTH,  side=TOP, anchor=W, expand=YES)
#                        self.frame2.grid(row=self.row, column=1,sticky='W')
        
                "if(len(self.list)>0):"
                if(len(self.p.getTab()[n])>0):

                    
                    self.listOfFiles.append(li)
                    self.f.pack()
                    self.f.grid(row=cptInsert, column=0,sticky='W')
                    cptInsert+=1
                    self.valTot.append(self.val)
                    self.namesTot.append(self.listeName)
                try:
                    for index in range(len(self.nub(self.listeName))):
                        self.val[index].set(self.getDefaultValue(li, "#define "+ self.nub(self.listeName)[index]))
                except:
                    self.parent.destroy()
                    try:
                        tkMessageBox.showerror("error"," no default value")
                    except TclError:
                        print 
                n+=1
        vbar=Scrollbar(self,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.ScrolledCanvas.yview)
        hbar=Scrollbar(self,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.ScrolledCanvas.xview)
        self.ScrolledCanvas.config(width=400,height=300)
        self.ScrolledCanvas.config( xscrollcommand=hbar.set ,yscrollcommand=vbar.set)
        
        self.ScrolledCanvas.pack(side=LEFT,expand=True,fill=BOTH)
        
        
        
        self.validate=Button(self.frameLabelFrames, text="validate",font=("Helvetica", 10),command=self.valider)
        self.validate.grid(row=cptInsert, column=0, padx=5, pady=5)
        
        self.ScrolledCanvas.create_window(10,10, window=self.frameLabelFrames)
        self.frameLabelFrames.update_idletasks()
        self.ScrolledCanvas.config(scrollregion=self.ScrolledCanvas.bbox('all'))
        self.pack()
        
        if ((self.exist==False)):
            self.parent.destroy()
            if (self.src=="apps"):
                tkMessageBox.showwarning("error"," no Application could be modified")
            else:
                tkMessageBox.showwarning("error"," no target could be modified")

        self.parent.resizable(width=False, height=False)
        
    def nub(self,inpt):
        seen = set()
        out = []
        for item in inpt:
            if item not in seen:
                seen.add(item)
                out.append(item)
        return out
        
    def valider (self):
        r=0
        for fichier in self.listOfFiles:
            cpt=0
            for i in self.nub(self.namesTot[r]):
                val1="#define "+ i
                s=self.valTot[r][cpt].get()
                val2="#define "+i+" "+str(s)
                self.replaceAll(fichier, val1, val2)
                cpt=cpt+1
            r+=1
        self.parent.destroy()
        
            
            
    def show(self,data):
       
        if(data=="Entry"):
            v=StringVar()
            self.nameWidgets.append(data)
            widget =  globals()[data](self.frame, textvariable=v)
            self.val.append(v)
        elif ((data=="Radiobutton") or(data=="Checkbutton")):
            widget =  globals()[data](self.frame2)           
        else:
            v=StringVar()
            widget =  globals()[data](self.frame,variable=v)
            self.val.append(v)
            self.nameWidgets.append(data)
            def wid(evt):
                pass
            
            widget.config(command=wid)
        widget.pack(padx=2,side=LEFT)
        widget.grid(column=self.column, row=self.row, sticky='W')
        self.index=self.index+1
        return widget
        
        

    def replaceAll(self,file,searchExp,replaceExp):
        found=False
        for line in fileinput.input(file, inplace=1):
            if searchExp in line:
                found=True
                searchExp=line[:len(line)-1]
                line = line.replace(searchExp,replaceExp)
            sys.stdout.write(line)
        if(not (found)):
            tkMessageBox.showwarning("error"," the define constant is not declared in the source file")
            
    def getDefaultValue(self,file,expr):
        
        fp = open (file, "r") 
        for l in fp.readlines ():
            if expr in l:
                list=l.split()
                n=len(list)-1
                self.v= l.split()[n]
        return self.v 
       
            

    def label(self, name ):
        widget = Label(self.frame, text=name)
        widget.pack(padx=2,side=LEFT)
        widget.grid(column=self.column, row=self.row, sticky='W')
        return widget
    
if __name__== "__main__":
    app =Configurer(None)
    app.mainloop( )
