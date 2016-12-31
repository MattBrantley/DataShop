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

    def verify(self):
        return True

class RingSettingsObject(SettingsObject):
    type = 'Ring Settings Object'

    def __init__(self, **kwargs):
        self.ringList = []
        self.default = 0

    def addSelection(self, text):
        self.ringList.append(text)
        return len(self.ringList)-1

    def setDefault(self, index):
        self.default = index

    def drawWidget(self):
        self.widget = QComboBox()
        for options in self.ringList:
            self.widget.addItem(options)

        self.widget.setCurrentIndex(self.default)
        return self.widget

    def getUserSetting(self):
        return str(self.widget.currentText())

class IntegerSettingsObject(SettingsObject):
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

    def drawWidget(self):
        self.widget = QSpinBox()
        self.widget.setMinimum(self.minimum)
        self.widget.setMaximum(self.maximum)
        self.widget.setValue(self.default)
        return self.widget

    def getUserSetting(self):
        return self.widget.value()

class FloatSettingsObject(SettingsObject):
    type = 'Float Settings Object'

    def __init__(self, **kwargs):
        self.minimum = kwargs.get('minimum', sys.float_info.min)
        self.maximum = kwargs.get('maximum', sys.float_info.max)
        self.decimals = kwargs.get('decimals', 4)
        self.default = kwargs.get('default', 1)

        self.lastVal = self.default

    def setMinimum(self, val):
        self.minimum = val

    def setMaximum(self, val):
        self.maximum = val

    def setDecimals(self, val):
        self.decimals = val

    def setDefault(self, val):
        self.default = val

    def drawWidget(self):
        self.widget = QLineEdit(str(self.default))
        self.validator = QDoubleValidator(self.minimum, self.maximum, self.decimals)
        self.widget.setValidator(self.validator)
        self.widget.textChanged.connect(self.verify)
        return self.widget

    def verify(self, string):
        if(string == '' or string == '-'):
            self.lastVal = 0
            return
        result = self.validator.validate(string, 0)
        if(result[0] == QValidator.Acceptable):
            self.lastVal = float(self.widget.text())
        else:
            self.widget.setText(str(self.lastVal))

    def getUserSetting(self):
        if(self.widget.text() == '-'):
            return 0.0
        elif(self.widget.text() == ''):
            return 0.0
        else:
            return float(self.widget.text())

class BoolSettingsObject(SettingsObject):
    type = 'Boolean Settings Object'

    def __init__(self, **kwargs):
        self.default = kwargs.get('default', False)

    def setDefault(self, val):
        self.default = val

    def drawWidget(self):
        self.widget = QCheckBox()
        self.widget.setChecked(self.default)
        return self.widget

    def getUserSetting(self):
        return self.widget.isChecked()

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