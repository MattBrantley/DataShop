import os, sys, imp, multiprocessing
from PyQt5.QtCore import Qt, QVariant, QTimer, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from UserScript import *
from UserScriptsController import *

class jobWidget(QWidget):
    WORKER_DATA = Qt.UserRole
    ACTIVE_FLAG = Qt.UserRole+1
    active = False

    def __init__(self, processList, name, worker):
        QWidget.__init__(self)
        self.worker = worker
        self.nameOP = 'Operation: ' + name
        self.drawWidget()
        self.jobWidgetItem = QListWidgetItem(processList)
        self.jobWidgetItem.setData(self.WORKER_DATA, worker)
        self.jobWidgetItem.setData(self.ACTIVE_FLAG, self.active)

        self.sizer = QSize()
        self.sizer.setHeight(26)

        self.jobWidgetItem.setSizeHint(self.sizer)
        self.jobWidgetItem.setIcon(QIcon('icons4\stop-1.png'))

    def setActive(self):
        self.active = True
        self.jobWidgetItem.setData(self.ACTIVE_FLAG, self.active)
        self.jobWidgetItem.setIcon(QIcon('icons4\hourglass-3.png'))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)

    def updateProgress(self, progress):
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(progress)

    def drawWidget(self):
        #self.setMaximumHeight(40)

        self.layout = QGridLayout()
        self.layout.setSpacing(1)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.nameFont = QFont()
        self.nameFont.setPointSize(8)
        self.nameWidget = QLabel(self.nameOP)
        self.nameWidget.setFont(self.nameFont)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximumHeight(16)

        self.layout.addWidget(self.nameWidget, 0, 0)
        self.layout.addWidget(self.progressBar, 1, 0)

        self.setLayout(self.layout)

    def getJobWidgetItem(self):
        return self.jobWidgetItem

class workerObj():
    jobActive = False
    killRequest = False
    ITEM_GUID = Qt.UserRole
    ITEM_TYPE = Qt.UserRole+1
    ITEM_NAME = Qt.UserRole+2

    def __init__(self, script, selectedItem, workspace, procManager):
        self.script = script
        self.selectedItem = selectedItem
        self.workspace = workspace
        self.procManager = procManager
        self.checkForSettings()

    def start(self, commMgr):
        self.commMgr = commMgr
        self.jobActive = True
        self.jobWidget.setActive()
        self.uScript = self.cloneScript(self.script)
        self.dOut = self.commMgr.dOut
        self.meta = self.commMgr.meta

        self.loadUserSettings()

        if(self.killRequest == False):
            self.process = multiprocessing.Process(group=None, name='Process Worker', target=self.uScript.start, args=(self.dOut, self.meta, self.uScript.settings, ))
            self.process.daemon = True
            self.process.start()

    def checkForSettings(self):
        if(self.script.settings):  #Settings were reserved by script - show settings window
            self.drawSettingWindow()
        else:                       #No settings were reserved by script - only use default settings
            self.loadDefaultSettings()

    def drawSettingWindow(self):
        self.dialogBox = QDialog(self.workspace.mainWindow)
        self.dialogBox.setModal(False)
        self.dialogBox.setMinimumWidth(300)
        self.dialogBox.setWindowTitle(self.script.name)
        self.dialogBox.setWindowIcon(QIcon('icons4\switch-4.png'))
        layout = QGridLayout()
        index = 0

        for key, setting in sorted(self.script.settings.items()):
            label = QLabel(key+':')
            tWidget = setting.drawWidget()
            if(setting.primaryEnabled == True):
                label = QLabel('*'+key+':')
                primaryName = str(self.selectedItem.text(0))
                #print(self.selectedItem)
                #print(self.selectedItem.text(0))
                primaryGUID = self.selectedItem.data(0, self.ITEM_GUID)
                tWidget.loadPrimaryDataSet(primaryName, primaryGUID)
            layout.addWidget(label, index, 0)
            layout.addWidget(tWidget, index, 1)
            index += 1

        self.okayButton = QPushButton('Accept')
        self.okayButton.clicked.connect(lambda: self.acceptSettingWindow())
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(lambda: self.rejectSettingWindow())
        layout.addWidget(self.okayButton, index, 0)
        layout.addWidget(self.cancelButton, index, 1)

        self.dialogBox.setLayout(layout)
        self.dialogBox.setVisible(True)

    def acceptSettingWindow(self):
        verList = {}
        for key, setting in self.script.settings.items():
            verified = setting.verify()
            if(verified == False):
                verList[key] = verified

        if(len(verList) > 0):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Settings Error!")
            msg.setStandardButtons(QMessageBox.Ok)
            stringOut = "Settings error for the following:"
            stringOut2 = ''
            for key in verList:
                stringOut2 = stringOut2 + key + '\n'

            msg.setText(stringOut)
            msg.setInformativeText(stringOut2)
            msg.exec_()
        else:
            self.dialogBox.close()
            self.procManager.addJobToQueue(self)

    def rejectSettingWindow(self):
        self.dialogBox.close()

    def loadDefaultSettings(self):
        for key, setting in self.script.settings.items():
            self.meta[key] = setting.default

    def loadUserSettings(self):
        for key, setting in self.script.settings.items():
            if(setting.type == 'DataSet Settings Object'):
                DataObjList = []
                GUIDList = setting.getUserSetting()
                for GUID in GUIDList:
                    tDataObj = ScriptIOData()
                    dataIn = self.workspace.loadDataByGUID(GUID)
                    tDataObj.matrix = dataIn
                    DataObjList.append(tDataObj)
                self.meta[key] = DataObjList
            else:
                self.meta[key] = setting.getUserSetting()

    def releaseMgr(self):
        self.commMgr.release()

    def loadInData(self, dataSet):
        dIn = self.commMgr.dIn
        tDataObj = ScriptIOData()
        tDataObj.matrix = dataSet
        dIn.append(tDataObj)
        return dIn

    def cloneScript(self, script):
        uScript = copy.deepcopy(script)
        uScript.clean()
        return uScript

    def createJobWidget(self, processList):
        self.jobWidget = jobWidget(processList, self.script.name, self)
        return self.jobWidget

    def removeJobWidget(self, processList):
        index = processList.row(self.jobWidget.getJobWidgetItem())
        processList.takeItem(index)

    def updateJobWidget(self):
        if 'Progress' in self.meta:
            self.jobWidget.progressInfo = True
            self.jobWidget.updateProgress(self.meta['Progress'])
        else:
            self.jobWidget.progressInfo = False

    def killSelf(self):
        self.killRequest = True
        self.process.terminate()

class procCommManager():
    inUse = False

    def __init__(self):
        self.mgr = multiprocessing.Manager()
        self.dOut = self.mgr.list()
        self.dIn = self.mgr.list()
        self.meta = self.mgr.dict()

    def assign(self):
        self.inUse = True

    def release(self):
        self.inUse = False
        self.clear()

    def clear(self):
        self.dOut = self.mgr.list()
        self.meta = self.mgr.dict()
        self.dIn = self.mgr.list()