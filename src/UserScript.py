import numpy as np, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep

class ScriptIOData():
    matrix = []
    name = 'Result'

class SettingsObject():
    type = 'Setting'

    def drawWidget(self):
        self.widgetReturnVal = QWidget()
        return self.widgetReturnVal

class IntegerSettingsObject():
    type = 'Integer Settings Object'

    def __init__(self, **kwargs):
        self.minimum = kwargs.get('minimum', -sys.maxsize - 1)
        self.maximum = kwargs.get('maximum', sys.maxsize)
        self.default = kwargs.get('default', 1)

    def setMinimum(self, val):
        self.minimum = val

    def setMaximum(self, val):
        self.maximum = val

    def setDefault(self, val):
        self.default = val

    def verify(self):
        if(self.default < self.minimum):
            return False
        elif(self.default > self.maximum):
            return False
        elif(type(self.default) == int):
            return False
        else:
            return True

    def drawWidget(self, mW):
        self.widgetReturnVal = QLineEdit(str(self.default))
        self.widgetReturnVal.setValidator(QIntValidator(self.minimum, self.maximum))
        return self.widgetReturnVal

    def getUserSetting(self):
        return int(self.widgetReturnVal.text())

class UserScript():
    name = 'Default'
    tooltip = 'Default Tool Tip'
    type = 'UserScript'
    url = ''
    settings = {}

    nDimension = -1
    nDataSets = -1

    def __init__(self, url):
        name = 'Default'
        self.url = url

    def getName(self):
        return self.name

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

    def start(self, dOut, dIn, meta, settings):
        self.settings = settings
        self.operation(dOut, dIn, meta)

    def operation(self, dOut, dIn, meta):
        print('Nothing Happened')