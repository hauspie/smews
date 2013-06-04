'''
Created on May 28, 2013

@author: rubi
'''
import os
class PathAndNames:
    def __init__(self, root):
        self.rootPath=os.path.join("..","..")
        self.apps = "apps"
        self.target="targets"
        self.script="run.sh"
        self.image="target.jpg"
        self.description="README"
