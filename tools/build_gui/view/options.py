import Tix
import glob 
import os.path 

from distutils.cmd import Command
from Tkinter import *

class OptionsUI(Tix.Frame):
    def __init__(self,parent):
        Tix.Frame.__init__(self,parent)
        self.parent=parent
        self.initialize()
        
    def initialize (self):
        self.grid()
        self.optionParams=[]
        self.options=[]
        self.frame1=Tix.Frame(self, bd=2)
        self.frame2=Tix.Frame(self, bd=2)
        self.frame3=Tix.Frame(self, bd=2)
        self.B=Tix.Radiobutton(self)
        L1 = Tix.Label(self.frame2, text="        ")
        L1.grid(column=0, row=0,sticky='W')
        L1 = Tix.Label(self.frame2, text="disable")
        L1.grid(column=1, row=0,sticky='W')
        L1 = Tix.Label(self.frame2, text="enable")
        L1.grid(column=2, row=0,sticky='W')
        self.disable=[]

        
        debug = Tix.Label(self.frame1, text="debug`")
        debug.grid(column=0, row=1,sticky='W',padx=5,pady=6)
        self.v_debug = Tix.StringVar()
        self.c1 = Tix.Radiobutton(self.frame1,text ="true",bd=5,variable=self.v_debug,value=0,anchor="e",padx=5) 
        self.c1.grid(column=1,row=1, sticky='W',padx=5,pady=5)   
        c2 = Tix.Radiobutton(self.frame1, text="false", variable=self.v_debug, value=1,anchor="e",padx=5)
        c2.grid(column=2,row=1, sticky='W',padx=5,pady=5)
        self.options.append(["debug",self.v_debug])
        self.c1.select()

        
        gzip = Tix.Label(self.frame1, text="gzip`")
        gzip.grid(column=0, row=2,sticky='W',padx=5,pady=5)
        
        self.v_gzip  = Tix.StringVar()
        c1 = Tix.Radiobutton(self.frame1, text="true", variable=self.v_gzip , value=0,anchor="e",padx=5)
        c1.grid(column=1,row=2, sticky='W',padx=5,pady=5)   
        c2 = Tix.Radiobutton(self.frame1, text="false", variable=self.v_gzip , value=1,anchor="e",padx=5)
        c2.grid(column=2,row=2, sticky='W',padx=5,pady=5)
        self.options.append(["gzip",self.v_gzip])
        c1.select()
        
        littleEnd = Tix.Label(self.frame1, text="endian")
        littleEnd.grid(column=0, row=3,sticky='W',padx=5,pady=5)
        
        self.v_endian  = Tix.StringVar()
        c1 = Tix.Radiobutton(self.frame1, text="little", variable=self.v_endian , value=0,anchor="e",padx=5 )
        c1.grid(column=1,row=3, sticky='W',padx=5,pady=5)   
        c2 = Tix.Radiobutton(self.frame1, text="big", variable=self.v_endian , value=1,anchor="e",padx=5)
        c2.grid(column=2,row=3, sticky='W',padx=5,pady=5)
        self.options.append(["endian",self.v_endian])
        c1.select()

        self.v_argument = Tix.StringVar()
        arg = Tix.Label(self.frame2, text="argument")
        arg.grid(column=0, row=1,sticky='W')
        argE = Tix.Radiobutton(self.frame2,text ="",bd=5,variable=self.v_argument,value=0,anchor="e",padx=5) 
        argE.grid(column=1,row=1, sticky='W')               
        argD = Tix.Radiobutton(self.frame2,text ="",bd=5,variable=self.v_argument,value=1,command=self.rep) 
        argD.grid(column=2,row=1) 
        argE.select()
        self.disable.append(["arguments",self.v_argument])
        self.v_comet = Tix.StringVar()
        comet = Tix.Label(self.frame2, text="comet")
        comet.grid(column=0, row=2,sticky='W')
        cometE = Tix.Radiobutton(self.frame2,text ="",bd=5,variable=self.v_comet,value=0,anchor="e",padx=5) 
        cometE.grid(column=1,row=2, sticky='W')               
        cometD= Tix.Radiobutton(self.frame2,text ="",bd=5,variable=self.v_comet,value=1) 
        cometD.grid(column=2,row=2) 
        cometE.select()
        self.disable.append(["comet",self.v_comet])
        self.v_retransmit = Tix.StringVar()
        retransmit = Tix.Label(self.frame2, text="retransmit")
        retransmit.grid(column=0, row=3,sticky='W')
        retransmitE= Tix.Radiobutton(self.frame2,text =" ",bd=5,variable=self.v_retransmit,value=0,anchor="e",padx=5) 
        retransmitE.grid(column=1,row=3,sticky='W')               
        retransmitD= Tix.Radiobutton(self.frame2,text ="",bd=5,variable=self.v_retransmit,value=1) 
        retransmitD.grid(column=2,row=3)   
        retransmitE.select()
        self.disable.append(["retransmit",self.v_retransmit])
        self.sum = Tix.StringVar()    
        checkSum = Tix.Label(self.frame3, text="chuncksNbits")
        checkSum.grid(column=0, row=5,sticky='W') 
        self.checkSum = Tix.ComboBox(self.frame3, editable=1, dropdown=1, variable=self.sum)
        self.options.append(["chuncksNbits",self.sum])
        self.checkSum.entry.config(state='readonly')
        for i in range(3,13):
            self.checkSum.insert(END,i )
        self.checkSum.grid(column=9,row=5)   


#        self.frame1.pack(fill=Tix.BOTH,  side=TOP, anchor=W, expand=YES)
        self.frame1.grid(row=2, column=0,sticky='W')
#        self.frame2.pack(fill=Tix.BOTH,  side=TOP, anchor=W, expand=YES)
        self.frame2.grid(row=4, column=0,sticky='W')
#        self.frame3.pack(fill=Tix.BOTH,  side=TOP, anchor=W, expand=YES)
        self.frame3.grid(row=6, column=0,sticky='W')
        
        
        
    def report(self):
        print "test"
    def rep(self):
        print "b2"
    
        
   
        
    def getOptionsParam(self):
        return self.optionParams
        
        
        
        
if __name__== "__main__":
    OptionsUI().mainloop( )






