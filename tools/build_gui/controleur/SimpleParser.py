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
    # extracts c file properties from its xml data
    # returns the file data
    def listdirectory(self,path): 
        fichier=[] 
        for root, dirs, files in os.walk(path): 
            for i in files:
                if(i.endswith(".c"))or (i.endswith(".h")): 
                    fichier.append(os.path.join(root, i)) 
        print fichier
        return fichier
    
    def extractPropsFromXml(self,srcFile):
        self.liste=[];
        self.name=[]
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
            print 'Start element:', name, attrs
        def end_element(name):
            print 'End element:', name
        def char_data(data):
            print 'Character data:', repr(data)
         
        p = xml.parsers.expat.ParserCreate()
        
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data
        # select the XML part of the c file
        xmlRoot = "groups"
       

        if fileData.rfind('<' + xmlRoot)<0:
            pass
        else:
            xmlData = fileData[fileData.rfind('<' + xmlRoot ):]
            xmlData = xmlData[:xmlData.rfind('</' + xmlRoot + '>') + len(xmlRoot) + 3]
            p.Parse(xmlData, 1)
        self.res=[]
        self.label=""
        for i in self.liste:
            self.l=[]

            for j in i:
                if(str( j)=="show"):
                    self.l.insert(0,[str( j),str(i[j])])
                else:
                    if(str( j)=="label"):
                        self.label=str(i[j])
                    self.l.append([str( j),str(i[j])])
                print "hhhhhhhhh", self.l

            self.res.append(self.l)
        print "here",self.label
        return  self.res[1:]
    
    def getLabelGroup(self):
        return self.label
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
        return keys
    
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
        print "vaaaaaaaaal", values
        return values
    
"""if __name__== "__main__":
    app=Parser()
    
    app.extractPropsFromXml("/home/rubi/Desktop/m1_s2/smews-master/apps/time/time.c")
    l=app.getValues()
    l1=app.getKeys()
    print "l",l
    print "l1",l1"""