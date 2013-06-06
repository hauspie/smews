class Profil:
    def __init__(self,target):
        self.tab=[]
        self.name=target

    def __unicode__(self):
        return "Profil: {0} -> {1}".format(self.name, self.tab)
    def __str__(self):
        return self.__unicode__()

    def getName(self):
        return self.name
    
    def getProfils(self):
        return self.tab
    
    def setTab(self,t):
        self.tab=t
        
    def setName(self,nom):
        self.name=nom
