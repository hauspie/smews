import os
import glob
import ttk
import Tkinter, tkFileDialog
import tkMessageBox, tkFileDialog
from Tkinter import *
import Tix

class ValidatingEntry(Entry):
    def __init__(self, master, value="", **kw):
        apply(Entry.__init__, (self, master), kw)
        self.__value = value
        self.__variable = StringVar()
        self.__variable.set(value)
        self.__variable.trace("w", self.__callback)
        self.config(textvariable=value, width=3)

    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(self.newvalue)
        else:
            self.__value = value

    def validate(self, value):
        return value
        
        
class MaxLengthEntry(ValidatingEntry):

    def __init__(self, master, defvalue=None, maxlength=None, **kw):
        self.maxlength = maxlength
        self.defvalue=defvalue
        apply(ValidatingEntry.__init__, (self, master), kw)

    def validate(self, value):
        if self.maxlength is None or len(value) <= self.maxlength :
            return value
        return None 
    
class AffichageIPV4(Tix.Frame):
    
    def __init__(self,frameIP):
        Tix.Frame.__init__(self,frameIP)
        self.fip=frameIP
        self.initialize()
        
        
    
    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(self.newvalue)
        else:
            self.__value = value
    
    def OnValidate(self,entree):
            
        if entree.get().isdigit() and int(entree.get())<=255 and int(entree.get())>=0 :
            return entree.get()
        else:
            
            self.signaleErreur(entree)
            return False 
       
 


    def signaleErreur(self,entree):

        entree.configure(bg ='red') 
         
    def initialize (self):
        self.grid()
        self.booleanOk=False
        "self=Tix.Frame(self.fip, bd=2)"
        frame1=Tix.Frame(self, bd=2)
        frame2=Tix.Frame(self, bd=2)
        frame3=Tix.Frame(self, bd=2)
        frame4=Tix.Frame(self, bd=2)
        framep1=Tix.Frame(self, bd=2)
        framep2=Tix.Frame(self, bd=2)
        framep3=Tix.Frame(self, bd=2)
        
        p1= Tix.Label(framep1,text=".",font ="Times 14 bold italic",fg="red",anchor=Tix.W)
        p2= Tix.Label(framep2,text=".",font ="Times 14 bold italic",fg="red",anchor=Tix.W)
        p3= Tix.Label(framep3,text=".",font ="Times 14 bold italic",fg="red",anchor=Tix.W)
        "adresse par defaut "
        self.valeur1 = Tix.StringVar()
        self.valeur1.set("192")
        self.valeur2 = Tix.StringVar()
        self.valeur2.set("168")
        self.valeur3 = Tix.StringVar()
        self.valeur3.set("1")
        self.valeur4 = Tix.StringVar()
        self.valeur4.set("2")
    
        self.E1= Tix.Entry(frame1,textvariable=self.valeur1, width=3)
        self.E1.configure(validate="focus",validatecommand=self.OnValidate(self.E1))
        self.E1.bind("<Return>", self.OnPressEnter)
        self.valeur1.set(u"192")
        self.E1.focus_set()
        self.E1.selection_range(0, Tix.END)
        self.E1.pack(padx=2,side=Tix.LEFT)
        self.E1.grid(column=2, row=1, sticky='W')
        frame1.grid(row=2, column=0)
        p1.grid(column=1, row=1)
        self.E1.focus()
        framep1.grid(row=2, column=1)

        self.E2= Tix.Entry(frame2,textvariable=self.valeur2, width=3)
        self.E2.configure(validate="focus",validatecommand=self.OnValidate(self.E2))
        self.E2.bind("<Return>", self.OnPressEnter)
        self.valeur1.set(u"192")
        self.E2.pack(padx=2,side=Tix.LEFT)
        self.E2.grid(column=2, row=1, sticky='W')
        frame2.grid(row=2, column=2)
        p2.grid(column=3, row=1, sticky='E')
        framep2.grid(row=2, column=3)


        self.E3= Tix.Entry(frame3,textvariable=self.valeur3, width=3)
        self.E3.configure(validate="focus",validatecommand=self.OnValidate(self.E3))
        self.E3.bind("<Return>", self.OnPressEnter)
        self.valeur1.set(u"192")
       
        self.E3.pack(padx=2,side=Tix.LEFT)
        self.E3.grid(column=2, row=1, sticky='W')
        frame3.grid(row=2, column=4)
        p3.grid(column=5, row=1)
        framep3.grid(row=2, column=5)
        self.f=Tix.Frame(self, bd=2)

        
        self.E4= Tix.Entry(frame4,textvariable=self.valeur4, width=3)
        self.E4.configure(validate="focus",validatecommand=self.OnValidate(self.E4))
        self.valeur1.set(u"192")
        self.E4.pack(padx=2,side=Tix.LEFT)
        self.E4.grid(column=2, row=1, sticky='W')
        frame4.grid(row=2, column=6)
        self.grid(row=2, column=2,sticky='W')
        self.error=False;

    
    def OnPressEnter(self,event):
        if self.focus_get()==self.E1 :
            if self.OnValidate(self.E1):
                self.E2.focus()
                self.E2.focus_set()
                self.E2.selection_range(0, Tix.END)
                self.E1.configure(bg='white')

            else :

                tkMessageBox.showwarning("error","please enter a number between 0 and 255")
                b=Tix.Balloon()
                b.bind_widget(self.E1, balloonmsg="please enter a number between 0 and 255")
                self.E1.focus_set()
                self.E1.selection_range(0, Tix.END)
                self.error=True;
               


        elif self.focus_get()==self.E2:
            if self.OnValidate(self.E2):
                self.E3.focus()
                self.E3.focus_set()
                self.E3.selection_range(0, Tix.END)
                self.E2.configure(bg='white')

            else :
                tkMessageBox.showwarning("error","please enter a number between 0 and 255")
                b=Tix.Balloon()
                b.bind_widget(self.E1, balloonmsg="please enter a number between 0 and 255")
                self.E2.focus_set()
                self.E2.selection_range(0, Tix.END)
                self.error=True;
                
        elif self.focus_get()==self.E3:
            if self.OnValidate(self.E3):
                self.E4.focus()
                self.E4.focus_set()
                self.E4.selection_range(0, Tix.END)
                self.E3.configure(bg='white')

            else :
                tkMessageBox.showwarning("error","please enter a number between 0 and 255")
                b=Tix.Balloon()
                b.bind_widget(self.E1, balloonmsg="please enter a number between 0 and 255")
                self.E3.focus_set()
                self.E3.selection_range(0, Tix.END)
                self.error=True;
                

        elif self.focus_get()==self.E4:
            if self.OnValidate(self.E4):
                self.getIpValue()
                self.booleanOk=True
                self.E4.configure(bg='white')

            else :
                tkMessageBox.showwarning("error","please enter a number between 0 and 255")
                b=Tix.Balloon()
                b.bind_widget(self.E1, balloonmsg="please enter a number between 0 and 255")
                self.E4.focus_set()
                self.E4.selection_range(0, Tix.END)
                self.error=True;
               
        if (self.error==True) :
            for w in self.f.winfo_children():
                w.destroy()
            self.error=False
    


    def getBooleanOk(self):
        return self.booleanOk
    
    def getIpValue(self):
        s=self.E1.get()+".";
        s=s+self.E2.get()+"."+self.E3.get()+"."+self.E4.get()
        return s