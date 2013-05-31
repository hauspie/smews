class NomValeur:
    def __init__(self,name,valeur):
        self.name=name
        self.valeur=valeur
        
    def getName(self):
        return self.name
    
    def getValeur(self):
        return self.valeur
    
    def setValeur(self,t):
        self.valeur=t
        
    def setName(self,nom):
        self.name=nom
        
class AppsConfig:
    def __init__(self,apps):
        self.name=apps
        self.args=[]
        
    def getName(self):
        return self.name
    
    def getArgs(self):
        return self.args
    
    def setArgs(self,t):
        self.args=t
        
    def setName(self,nom):
        self.name=nom