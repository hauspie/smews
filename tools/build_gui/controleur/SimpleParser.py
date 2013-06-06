'''
Created on 25 mars 2013

@author: jomaa
'''
import xml.parsers.expat
import os
import re
class Parser:
    def __init__(self):
        self.postList = []
        self.liste=[];

    # extracts c file properties from its xml data
    # returns the file data
    def listdirectory(self,path): 
        fichier=[] 
        for root, dirs, files in os.walk(path): 
            for i in files:
                if(i.endswith(".c"))or (i.endswith(".h")): 
                    fichier.append(os.path.join(root, i)) 
        return fichier
    
    def compterLesGroupes(self,file,root):
        cpt=0
        f = open(file,'r')
        for line in f:
            if root in line:
                cpt+=1
        return cpt/2
    def extractPropsFromXml(self,srcFile):
        self.liste=[];
        self.name=[]
        self.labels=[]
        # open the source file in order to parse the XML and return the file data
        self.file = open(srcFile,'r')
        lines = self.file.readlines()
        if len(lines) > 1:
            fileData = reduce(lambda x,y: x + y,lines)
        else:
            fileData = ''
        # 3 handler functions
        def start_element(name, attrs):
            
            self.name.append(str(name))
            self.liste.append(attrs)
        def end_element(name):
            pass
        def char_data(data):
            pass
        p = xml.parsers.expat.ParserCreate()
        
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data
        # select the XML part of the c file
        xmlRoot = "config"
       

        if fileData.rfind('<' + xmlRoot)<0:
            pass
        else:
            
            xmlData = fileData[fileData.rfind('<'+xmlRoot):]
            xmlData = xmlData[:xmlData.rfind('</' + xmlRoot + '>') + len(xmlRoot) + 3]
            p.Parse(xmlData, 1)
            
        self.res=[]
        self.label=""
        self.tab=[]
        self.lesCles=[]
        self.lesvals=[]

        for i in self.liste:
            self.l=[]

            for j in i:
                if(str( j)=="show"):
                    self.l.insert(0,[str( j),str(i[j])])
                else:
                    if(str( j)=="label"):
                        self.label=str(i[j])
                        self.labels.append(self.label)

                    self.l.append([str( j),str(i[j])])

            self.res.append(self.l)
        j=0
        k=0
        
        for i in self.res[2:]:
            if len(i)>0:
                
                if (i[0][0]=="label"):

                    self.tab.append(self.res[1:][k:j+1])
                    
                    j+=1
                    k=j
                elif (j==len(self.res[2:])-1):
                    self.tab.append(self.res[1:][k:])
                else :
                    j+=1
            else :
                j+=1

        return  self.res[1:]
    
    def getTab(self):
        return self.tab
    def getLabelGroup(self):
        return self.labels
    def getKeys(self):
        keys=[]
        
        for  k in self.liste[1:]:
            self.tabk=[]
            for j in range(len(k.keys())):
                if (str(k.keys()[j])=='show'):
                    self.tabk.insert(0, str(k.keys()[j]))
                else:
                    self.tabk.append(str(k.keys()[j]))
           
            keys.append(self.tabk)
            
        j=1
        k=0
        
        for i in keys[1:]:
            if len(i)>0:
                if (i[0]=="label"):
                    self.lesCles.append(keys[k:j])
                    j+=1
                    k=j
                elif (j==len(keys)-1):
                    self.lesCles.append(keys[k-1:])
                else :
                    j+=1
            else :
                j+=1

        return keys
    def getLesCles(self):
        return self.lesCles
    
    def getLesVals(self):
        return self.lesvals
    def getValues(self):
        values=[]
        cpt=1
        for  k in self.liste[1:]:
            self.tabk=[]
            t=[]
            for j in range(len(k.values())):
                if (str(k.keys()[j])=='show'):
                    self.tabk.insert(0, str(k.values()[j]))
                else:
                    self.tabk.append(str(k.values()[j]))
            t.append(str(self.name[cpt]))
            values.append([t,self.tabk])
            cpt=cpt+1
        j=1
        k=0
        
        for i in values[1:]:
            if len(i)>0:

                if (i[0][0]=="groups"):
                    self.lesvals.append(values[k:j])
                    j+=1
                    k=j
                elif (j==len(values)-1):
                    self.lesvals.append(values[k-1:])
                else :
                    j+=1
            else :
                j+=1

        return values
    
if __name__== "__main__":
    app=Parser()
    
    s=app.extractPropsFromXml("/home/rubi/Desktop/m1_s2/smews-master/apps/time/time.c")
    l=app.getValues()
    l1=app.getKeys()
