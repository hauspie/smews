from .pathNamesConfig import PathAndNames

import os

def get():
    targets = {}
    for t in os.listdir(os.path.join(PathAndNames.rootPath, PathAndNames.target)):
        if "_" in t:
            t,sep,profil = t.partition("_")
        else:
            profil = []

        if t in targets:
            targets[t].append(profil)
        else:
            targets[t] = profil
    return targets
