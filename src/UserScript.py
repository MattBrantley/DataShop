import numpy as np
from time import sleep

class ScriptIOData():
    matrix = []

class UserScript():
    name = 'Default'
    tooltip = 'Default Tool Tip'
    type = 'UserScript'
    url = ''

    nDimension = -1
    nDataSets = -1

    def __init__(self, url):
        name = 'Default'
        self.url = url

    def printName(self):
        print(self.name)

    def getName(self):
        return self.name

    def printURL(self):
        print(self.url)

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

    def start(self, dOut, dIn, meta):
        self.operation(dOut, dIn, meta)

    def operation(self, dOut, dIn, meta):
        print('Nothing Happened')