
class AppsParam:
    def __init__(self,name,URL):
        self.name=name
        self.URL=URL
    def get_name(self):
        return self.__name


    def get_url(self):
        return self.__URL


    def set_name(self, value):
        self.__name = value


    def set_url(self, value):
        self.__URL = value

    name = property(get_name, set_name, None, None)
    URL = property(get_url, set_url, None, None)
