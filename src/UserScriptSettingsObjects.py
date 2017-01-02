from UserScript import *

class SettingsObject():
    type = 'Setting'
    primaryEnabled = False

    def drawWidget(self):
        self.widgetReturnVal = QWidget()
        return self.widgetReturnVal

    def verify(self):
        return True

    def setDescription(self, string):
        print('This setting object does not support tool tips.')

class RingSettingsObject(SettingsObject):
    type = 'Ring Settings Object'

    def __init__(self, **kwargs):
        self.ringList = []
        self.default = 0
        self.description = kwargs.get('description', 'N/A')

    def addSelection(self, text):
        self.ringList.append(text)
        return len(self.ringList)-1

    def setDefault(self, index):
        self.default = index

    def setDescription(self, string):
        self.description = string

    def renderToolTipString(self):
        return 'Description: ' + self.description + '\nCount: ' + str(self.widget.count()) + '\nDefault: ' +  self.widget.itemText(self.default)

    def drawWidget(self):
        self.widget = QComboBox()
        for options in self.ringList:
            self.widget.addItem(options)

        self.widget.setCurrentIndex(self.default)
        self.widget.setWhatsThis(self.renderToolTipString())
        return self.widget

    def getUserSetting(self):
        return str(self.widget.currentText())

class IntegerSettingsObject(SettingsObject):
    type = 'Integer Settings Object'

    def __init__(self, **kwargs):
        self.minimum = kwargs.get('minimum', -sys.maxsize - 1)
        self.maximum = kwargs.get('maximum', sys.maxsize)
        self.default = kwargs.get('default', 1)
        self.description = kwargs.get('description', 'N/A')

    def setMinimum(self, val):
        self.minimum = val

    def setMaximum(self, val):
        self.maximum = val

    def setDefault(self, val):
        self.default = val

    def setDescription(self, string):
        self.description = string

    def renderToolTipString(self):
        return 'Description: ' + self.description + '\nMinimum: ' + str(self.minimum) + '\nMaximum: ' + str(self.maximum) + '\nDefault: ' + str(self.default)

    def drawWidget(self):
        self.widget = QSpinBox()
        self.widget.setMinimum(self.minimum)
        self.widget.setMaximum(self.maximum)
        self.widget.setValue(self.default)
        self.widget.setWhatsThis(self.renderToolTipString())
        return self.widget

    def getUserSetting(self):
        return self.widget.value()

class FloatSettingsObject(SettingsObject):
    type = 'Float Settings Object'

    def __init__(self, **kwargs):
        self.minimum = kwargs.get('minimum', -1E50) #Arbitrary value since sys max in python differs from C++
        self.maximum = kwargs.get('maximum', 1E50) #Arbitrary value since sys max in python differs from C++
        self.decimals = kwargs.get('decimals', 4)
        self.default = kwargs.get('default', 1)
        self.description = kwargs.get('description', 'N/A')

        self.lastVal = self.default

    def setMinimum(self, val):
        self.minimum = val

    def setMaximum(self, val):
        self.maximum = val

    def setDecimals(self, val):
        self.decimals = val

    def setDefault(self, val):
        self.default = val

    def setDescription(self, string):
        self.description = string

    def renderToolTipString(self):
        return 'Description: ' + self.description + '\nNum Decimals: ' + str(self.decimals) + '\nMinimum: ' + str(self.minimum) + '\nMaximum: ' + str(self.maximum) + '\nDefault: ' + str(self.default)

    def drawWidget(self):
        self.widget = QLineEdit(str(self.default))
        self.validator = QDoubleValidator(self.minimum, self.maximum, self.decimals)
        self.widget.setValidator(self.validator)
        self.widget.textChanged.connect(self.validate)
        self.widget.setWhatsThis(self.renderToolTipString())
        return self.widget

    def validate(self, string):
        if(string == '' or string == '-'):
        #    self.lastVal = 0
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
        self.description = kwargs.get('description', 'N/A')

    def setDefault(self, val):
        self.default = val

    def setDescription(self, string):
        self.description = string

    def renderToolTipString(self):
        return 'Description: ' + self.description + '\nDefault: ' + str(self.default)

    def drawWidget(self):
        self.widget = QCheckBox()
        self.widget.setChecked(self.default)
        self.widget.setWhatsThis(self.renderToolTipString())
        return self.widget

    def getUserSetting(self):
        return self.widget.isChecked()

class StringSettingsObject(SettingsObject):
    type = 'String Settings Object'

    def __init__(self, **kwargs):
        self.default = kwargs.get('default', '')
        self.description = kwargs.get('description', 'N/A')

    def setDefault(self, string):
        self.default = str(string)

    def setDescription(self, string):
        self.description = string

    def renderToolTipString(self):
        return 'Description: ' + self.description + '\nDefault: ' + str(self.default)

    def drawWidget(self):
        self.widget = QLineEdit(str(self.default))
        self.widget.setWhatsThis(self.renderToolTipString())
        return self.widget

    def getUserSetting(self):
        return str(self.widget.text())

class DataSetSettingsObject(SettingsObject):
    type = 'DataSet Settings Object'

    def __init__(self, **kwargs):
        self.maximum = kwargs.get('maximum', 1)
        self.minimum = kwargs.get('minimum', 0)
        self.numDims = kwargs.get('numDims', [0])
        self.description = kwargs.get('description', 'N/A')
        self.primaryEnabled = kwargs.get('primaryEnabled', False)

    def setMaximum(self, val):
        self.maximum = val

    def setMinimum(self, val):
        self.minimum = val

    def setNumDims(self, val):
        self.numDims = val

    def setDescription(self, string):
        self.description = string

    def renderToolTipString(self):
        if(self.primaryEnabled):
            return 'Description: ' + self.description + '\n[PRIMARY ENABLED]' + '\nMinimum Count: ' + str(self.minimum) + '\nMaximum Count: ' + str(self.maximum)
        else:
            return 'Description: ' + self.description + '\nMinimum Count: ' + str(self.minimum) + '\nMaximum Count: ' + str(self.maximum)

    def drawWidget(self):
        if(self.primaryEnabled == True):
            self.maximum = 1
            self.minimum = 1

        self.widget = DataSetSettingWidget(self.maximum, self.minimum, self.numDims, self.primaryEnabled)
        self.widget.setWhatsThis(self.renderToolTipString())

        return self.widget

    def verify(self):
        if(self.widget.countFillerItems() == 0):
            return True
        else:
            return False

    def getUserSetting(self):
        vals = self.widget.returnValues()
        del self.widget # This actually stop the memory management issue for self contained settings.
        return vals

class DataSetSettingWidget(QListWidget):
    ITEM_GUID = Qt.UserRole
    ITEM_TYPE = Qt.UserRole+1
    ITEM_NAME = Qt.UserRole+2
    primaryLoaded = False

    FILLER_TYPE_REQ = 200

    def __init__(self, numSets, minSets, numDims, primaryEnabled):
        super().__init__()
        self.numSets = numSets
        self.minSets = minSets
        self.numDims = numDims
        self.primaryEnabled = primaryEnabled

        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        #Matt's Hacky-Sacky way of determining row sizes!
        self.addItem('')
        self.rowSizeHint = self.sizeHintForRow(0)
        self.takeItem(0)
        #

        if(self.numSets <= 10):
            self.setMaximumHeight(self.rowSizeHint*self.numSets + 4)
        else:
            self.setMaximumHeight(self.rowSizeHint*10 + 4)

        self.drawFillerItems()

    def countFillerItems(self):
        idx = 0
        fillCount = 0
        for item in range(self.count()):
            item = self.item(idx)
            if(item.data(self.ITEM_TYPE) == self.FILLER_TYPE_REQ):
                fillCount += 1
            idx += 1
        return fillCount

    def countNonFillerItems(self):
        idx = 0
        nonFillCount = 0
        for item in range(self.count()):
            item = self.item(idx)
            if(item.data(self.ITEM_TYPE) is not self.FILLER_TYPE_REQ):
                nonFillCount += 1
            idx += 1
        return nonFillCount

    def drawFillerItems(self):
        count = self.countNonFillerItems()
        reqItemRem = self.minSets - count
        if(reqItemRem < 0):
            reqItemRem = 0

        for idx in range(reqItemRem):
            reqItem = QListWidgetItem('Required Data Set...')
            reqItem.setData(self.ITEM_TYPE, self.FILLER_TYPE_REQ)
            reqItem.setBackground(Qt.red)
            self.addItem(reqItem)

    def checkReqItemFillers(self):
        count = self.count()
        for idx in range(count):
            revIDX = count-idx-1
            item = self.item(revIDX)
            if(item.data(self.ITEM_TYPE) == self.FILLER_TYPE_REQ):
                self.takeItem(revIDX)
        self.drawFillerItems()

    def removeItem(self, selectedItem):
        index = self.row(selectedItem[0])
        self.takeItem(index)
        self.checkReqItemFillers()
        self.setStyleSheet("""QListWidget{ background: rgb(255,255,255); }""")

    def contextMenu(self, position):
        # WARNING: Keep as little as possible (especially for QT objects) in memory or feel the wrath of multiproc's pickle! (Not joking)
        if(self.primaryLoaded == False):
            if(self.selectedItems()):
                selectedItem = self.selectedItems()
                if(selectedItem[0].data(self.ITEM_TYPE) != self.FILLER_TYPE_REQ):
                    removeAction = QAction(QIcon('icons\\transfer-1.png'),'Remove', self)
                    removeAction.setStatusTip('Remove this dataSet')
                    removeAction.triggered.connect(lambda: self.removeItem(selectedItem))

                    contextMenu = QMenu()
                    contextMenu.addAction(removeAction)
                    contextMenu.exec_(self.viewport().mapToGlobal(position))
        else:
            primaryEnabledAction = QAction('This setting cannot be changed.', self)
            primaryEnabledAction.setEnabled(False)
            contextMenu = QMenu()
            contextMenu.addAction(primaryEnabledAction)
            contextMenu.exec_(self.viewport().mapToGlobal(position))

    def returnValues(self):
        guidList = []
        for idx in range(self.count()):
            if(self.item(idx).data(self.ITEM_TYPE) is not self.FILLER_TYPE_REQ):
                guidList.append(self.item(idx).data(self.ITEM_GUID))
        return guidList

    def loadPrimaryDataSet(self, name, GUID):
        self.primaryLoaded = True
        self.setAcceptDrops(False)
        self.clear()

        dataObj = QListWidgetItem(name)
        dataObj.setData(self.ITEM_GUID, GUID)
        dataObj.setBackground(Qt.lightGray)
        #dataObj.setForeground(Qt.darkGray)
        self.addItem(dataObj)

    def dropEvent(self, event):
        if(self.countNonFillerItems() < self.numSets):
            treeWidget = event.source() # WARNING: Do not store this in meory - will cause multiproc's pickle event to freak out!
            type = treeWidget.currentItem().data(0, self.ITEM_TYPE)
            name = treeWidget.currentItem().data(0, self.ITEM_NAME)
            GUID = treeWidget.currentItem().data(0, self.ITEM_GUID)

            if(type == 'Data'):
                dataObj = QListWidgetItem(name)
                dataObj.setData(self.ITEM_GUID, GUID)
                dataObj.setBackground(Qt.white)
                self.addItem(dataObj)
                self.checkReqItemFillers()

            if(self.countNonFillerItems() == self.numSets):
                self.setStyleSheet("""QListWidget{ background: rgb(220,220,220); }""")
