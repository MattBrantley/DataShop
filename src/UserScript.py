class UserScript():
    name = 'Default'
    type = 'UserScript'
    url = ''

    def __init__(self):
        name = 'Default'

    def printName(self):
        print(self.name)

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