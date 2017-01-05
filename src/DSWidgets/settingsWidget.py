from PyQt5.Qt import *

class settingsDefaultImporterListWidget(QWidget):
    def __init__(self, ext, importers, defImporter):
        QWidget.__init__(self)
        self.ext = ext
        self.importers = importers
        self.defImporter = defImporter
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.comboBox = QComboBox()

        layout.addWidget(QLabel('(*' + ext.lower() + '):'))
        layout.addWidget(self.comboBox)

        index = 0
        for importer in importers:
            self.comboBox.addItem(importer.name)
            if(importer.name == defImporter):
                self.comboBox.setCurrentIndex(index)
            index += 1

    def getNameOfSelected(self):
        return self.comboBox.currentText()

class settingsDockWidget(QDockWidget):
    def __init__(self, mainWindow):
        super().__init__("Settings")
        self.settingsContainer = QWidget()
        self.settingsLayout = QVBoxLayout()
        self.settingsWidget = QTabWidget()
        self.mainWindow = mainWindow

        self.settingsApplyButton = QPushButton('Apply')
        self.settingsApplyButton.clicked.connect(self.getNewSettings)

        self.settingsLayout.addWidget(self.settingsWidget)
        self.settingsLayout.addWidget(self.settingsApplyButton)
        self.settingsLayout.setSpacing(0)
        self.hide()

        self.settingsContainer.setLayout(self.settingsLayout)
        self.setWidget(self.settingsContainer)

        self.settingsGeneral = QWidget()
        self.settingsImporters = self.drawImportersSettingsTab()

        self.settingsWidget.addTab(self.settingsGeneral, 'General')
        self.settingsWidget.addTab(self.settingsImporters, 'Importers')

    def drawImportersSettingsTab(self):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        container.setLayout(layout)

        self.importSettingsWidgetList = []
        for ext, importers in sorted(self.mainWindow.workspace.userScripts.registeredImportersList.items()):
            defaultItem = settingsDefaultImporterListWidget(ext, importers, self.mainWindow.workspace.settings['Default Importers'][ext])
            self.importSettingsWidgetList.append(defaultItem)
            layout.addWidget(defaultItem)

        return container

    def getNewSettings(self):
        for defaultItem in self.importSettingsWidgetList:
            self.mainWindow.workspace.settings['Default Importers'][defaultItem.ext.upper()] = defaultItem.getNameOfSelected()
        self.mainWindow.workspace.updateSettings()