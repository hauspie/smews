class Profil:
    def __init__(self,target):
        self.tab=[]
        self.name=target
        
    def getName(self):
        return self.name
    
    def getProfils(self):
        return self.tab
    
    def setTab(self,t):
        self.tab=t
        
    def setName(self,nom):
        self.name=nom