class UserScript():
    name = 'Default'
    tooltip = 'Default Tool Tip'
    type = 'UserScript'
    url = ''

    def __init__(self, url):
        name = 'Default'
        self.url = url

    def printName(self):
        print(self.name)

    def getName(self):
        return self.name

    def printURL(self):
        print(self.url)

class UserDisplay(UserScript):
    type = 'Display'

class UserExport(UserScript):
    type = 'Export'

class UserGenerator(UserScript):
    type = 'Generator'

class UserImport(UserScript):
    type = 'Import'

class UserInteract(UserScript):
    type = 'Interact'

class UserOperation(UserScript):
    type = 'Operation'

    def operation(self):
        print('Nothing Happened')