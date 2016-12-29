class ScriptIOData():
    matrix = []

class UserScript():
    name = 'Default'
    tooltip = 'Default Tool Tip'
    type = 'UserScript'
    url = ''

    nDimension = -1
    nDataSets = -1

    DataIn = []
    DataOut = []

    def __init__(self, url):
        name = 'Default'
        self.url = url

    def printName(self):
        print(self.name)

    def getName(self):
        return self.name

    def printURL(self):
        print(self.url)

    def loadData(self, dataSet):
        tDataObj = ScriptIOData()
        tDataObj.matrix = dataSet
        self.DataIn.append(tDataObj)

    def retrieveData(self):
        return self.DataOut

    def clean(self):
        self.DataIn = []
        self.DataOut = []

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