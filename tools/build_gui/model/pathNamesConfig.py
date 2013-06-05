'''
Created on May 28, 2013

@author: rubi
'''
import os
class PathAndNames:
    def __init__(self, root):
        self.rootPath=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..",".."))
        print(self.rootPath)
        self.apps = "apps"
        self.target="targets"
        self.run_script="run.sh"
        self.kill_script="kill.sh"
        self.image="target.jpg"
        self.description="README"
