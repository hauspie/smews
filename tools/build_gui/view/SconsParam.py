'''
Created on 18 mars 2013

@author: jomaa
'''
class SconsParam:
    def __init__(self,ip,target,apps,options):
        self.ip=ip
        self.target=target
        self.apps=apps
        self.options=options

    def get_ip(self):
        return self.__ip


    def get_target(self):
        return self.__target


    def get_apps(self):
        return self.__apps


    def get_options(self):
        return self.__options


    def set_ip(self, value):
        self.__ip = value


    def set_target(self, value):
        self.__target = value


    def set_apps(self, value):
        self.__apps = value


    def set_options(self, value):
        self.__options = value


    def del_ip(self):
        del self.__ip


    def del_target(self):
        del self.__target


    def del_apps(self):
        del self.__apps


    def del_options(self):
        del self.__options

    ip = property(get_ip, set_ip, del_ip, "ip's docstring")
    target = property(get_target, set_target, del_target, "target's docstring")
    apps = property(get_apps, set_apps, del_apps, "apps's docstring")
    options = property(get_options, set_options, del_options, "options's docstring")
        
 
