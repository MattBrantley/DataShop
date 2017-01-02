import numpy as np, sys, copy
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

class DataSetSettingsObject(SettingsObject):
    type = 'DataSet Settings Object'

    def __init__(self, **kwargs):
        self.count = kwargs.get('count', 1)
        self.numDims = kwargs.get('numDims', [0])

    def setCount(self, val):
        self.count = val

    def setNumDims(self, val):
        self.numDims = val

    def drawWidget(self):
        self.widget = DataSetSettingWidget(self.count, self.numDims)
        return self.widget

    def getUserSetting(self):
        vals = self.widget.returnValues()
        del self.widget # This actually stop the memory management issue for self contained settings.
        return vals

class DataSetSettingWidget(QListWidget):
    ITEM_GUID = Qt.UserRole
    ITEM_TYPE = Qt.UserRole+1
    ITEM_NAME = Qt.UserRole+2

    def __init__(self, numSets, numDims):
        super().__init__()
        self.numSets = numSets
        self.numDims = numDims

        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

    def removeItem(self, selectedItem):
        index = self.row(selectedItem[0])
        self.takeItem(index)

    def contextMenu(self, position):
        # WARNING: Keep as little as possible (especially for QT objects) in memory or feel the wrath of multiproc's pickle! (Not joking)
        if(self.selectedItems()):
            selectedItem = self.selectedItems()
            removeAction = QAction(QIcon('icons\\transfer-1.png'),'Remove', self)
            removeAction.setStatusTip('Remove this dataSet')
            removeAction.triggered.connect(lambda: self.removeItem(selectedItem))

            contextMenu = QMenu()
            contextMenu.addAction(removeAction)
            contextMenu.exec_(self.viewport().mapToGlobal(position))

    def returnValues(self):
        guidList = []
        for idx in range(self.count()):
            guidList.append(self.item(idx).data(self.ITEM_GUID))
        return guidList

    def dropEvent(self, event):
        if(self.count() < self.numSets):
            treeWidget = event.source() # WARNING: Do not store this in meory - will cause multiproc's pickle event to freak out!
            type = treeWidget.currentItem().data(0, self.ITEM_TYPE)
            name = treeWidget.currentItem().data(0, self.ITEM_NAME)
            GUID = treeWidget.currentItem().data(0, self.ITEM_GUID)

            if(type == 'Data'):
                dataObj = QListWidgetItem(name)
                dataObj.setData(self.ITEM_GUID, GUID)
                self.addItem(dataObj)

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

    def start(self, dOut, meta, settings):
        self.settings = settings
        self.operation(dOut, meta)

    def operation(self, dOut, meta):
        print('Nothing Happened')