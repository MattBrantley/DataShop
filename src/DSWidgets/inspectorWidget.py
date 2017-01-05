from PyQt5.Qt import *

class inspectorDockWidget(QDockWidget):
    ITEM_GUID = Qt.UserRole

    def __init__(self, mainWindow):
        super().__init__('Inspector')
        self.inspectorContainer = QWidget()
        self.inspectorLayout = QVBoxLayout()

        self.hide()

        self.inspectorContainer.setLayout(self.inspectorLayout)
        self.setWidget(self.inspectorContainer)

        self.mainWindow = mainWindow

    def drawInspectorWidget(self, selectedItem):
        while self.inspectorLayout.count():
            child = self.inspectorLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        GUID = selectedItem.data(0, self.ITEM_GUID)
        DataSet = self.mainWindow.workspace.getScriptIODataFromSQLByGUID(GUID)


        self.inspectorLayout.addWidget(QLabel('Name: ' + DataSet.name))
        self.inspectorLayout.addWidget(QLabel('Shape: ' + str(DataSet.matrix.shape)))
        idx = 0
        for axis in DataSet.axes:
            self.inspectorLayout.addWidget(QLabel('Axis #' + str(idx)))
            self.inspectorLayout.addWidget(QLabel('    Name: ' + axis.name))
            if(axis.prefix is not None):
                self.inspectorLayout.addWidget(QLabel('    Units (Long): ' + axis.prefix.prefixText + axis.units.baseUnit))
                self.inspectorLayout.addWidget(QLabel('    Units (Short): ' + axis.prefix.prefixSymbol + axis.units.baseUnitSymbol))
            else:
                self.inspectorLayout.addWidget(QLabel('    Units: ' + axis.units.baseQuantity))
            self.inspectorLayout.addWidget(QLabel('    Base Quantity: ' + axis.units.baseQuantity))
            if(axis.prefix is not None):
                self.inspectorLayout.addWidget(QLabel('    Prefix: ' + axis.prefix.prefixText))
            else:
                self.inspectorLayout.addWidget(QLabel('    Prefix: None'))
            self.inspectorLayout.addWidget(QLabel('    Length: ' + str(axis.vector.shape[0])))
            idx += 1