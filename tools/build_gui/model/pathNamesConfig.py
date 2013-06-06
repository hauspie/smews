'''
Created on May 28, 2013

@author: rubi
'''
import os
class PathAndNames:
    rootPath=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..",".."))
    apps = "apps"
    target="targets"
    run_script="run.sh"
    kill_script="kill.sh"
    image="target.jpg"
    description="README"
