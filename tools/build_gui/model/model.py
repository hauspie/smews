import observable

class Model:
    def __init__(self):
        self.myModel = observable.Observable("192.168.1.4")
        
    def addTargetParams(self, targetParams):
        self.myModel.set(targetParams)
    
    """def addAppsParams(self, AppsParams): 
        self.myModel.get()[1].set(AppsParams)
        
    def addOptionsParams(self, optionsParams): 
        self.myModel.get()[2].set(optionsParams)"""
        
