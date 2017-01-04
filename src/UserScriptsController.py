import os, sys, imp, multiprocessing, functools
from PyQt5.QtCore import Qt, QVariant, QTimer, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from UserScript import *
from WorkerObjects import *

class scriptProcessManager():
    numWorkers = 4
    activeWorkers = []
    managers = []
    tickLength = 50 # Time between worker update cycles (This can slow down dramatically if the main thread lags)

    def __init__(self, workspace):
        self.workspace = workspace
        self.queueUpdateTimer = QTimer()
        self.initTimer()
        self.initProcessWidget()

        print('Building I/O Managers... ', end="", flush=True)
        for i in range (0, self.numWorkers):
            self.managers.append(procCommManager())
            self.managers[i].clear()
        print('Done!')

    def getAvailManager(self):
        for mgr in self.managers:
            if(mgr.inUse is False):
                return mgr

    def initProcessWidget(self):
        self.processWidget = QDockWidget("Process Queue", self.workspace.mainWindow)
        self.processWidget.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)

        self.processList = QListWidget(self.workspace.mainWindow)
        self.processList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.processList.customContextMenuRequested.connect(self.openMenu)

        self.processWidget.setWidget(self.processList)
        self.workspace.mainWindow.addDockWidget(Qt.RightDockWidgetArea, self.processWidget)

    def addProcessToWidget(self, job):
        newJobWidget = job.createJobWidget(self.processList)
        self.processList.addItem(newJobWidget.getJobWidgetItem())
        self.processList.setItemWidget(newJobWidget.getJobWidgetItem(), newJobWidget)

    def initDefaultContextMenu(self):
        selectedItem = self.processList.currentItem()
        selectedRow = self.processList.currentRow()
        itemWorker = selectedItem.data(Qt.UserRole)

        warningAction = QAction(QIcon('icons4\multiply-1'), 'Kill Job', self.workspace.mainWindow)
        warningAction.setStatusTip('Kill the selected job. (Note: No data will be returned)')
        warningAction.triggered.connect(lambda: self.abortJob(itemWorker))
        warningAction.setEnabled(True)

        self.contextMenu = QMenu()
        self.contextMenu.addAction(warningAction)

    def openMenu(self, position):
        if(self.processList.selectedItems()):
            self.initDefaultContextMenu()
            self.contextMenu.exec_(self.processList.viewport().mapToGlobal(position))

    def initTimer(self):
        self.queueUpdateTimer.timeout.connect(lambda: self.updateQueueWorkers())
        self.queueUpdateTimer.start(self.tickLength)

    def createJobForQueue(self, uScript, selectedItem):
        worker = workerObj(uScript, selectedItem, self.workspace, self) #Worker will run and then return addJobToQueue if successful

    def addJobToQueue(self, worker):
        self.addProcessToWidget(worker)

    def getNextAvailableWorker(self):
        for widgetItem in self.processList.findItems('', Qt.MatchRegExp):
            #worker = widgetItem.data(Qt.UserRole)
            active = widgetItem.data(Qt.UserRole+1)
            if(active == False):
                return widgetItem.data(Qt.UserRole)

    def startNextWorker(self):
        worker = self.getNextAvailableWorker()
        if(worker is not None):
            tMgr = self.getAvailManager()
            if(tMgr is not None):
                tMgr.assign()
                worker.start(tMgr)
                return worker
            else:
                print('CRITICAL ERROR: A manager has not been released somewhere! Aborting job!!!')
                self.abortJob(worker)
                return None

    def updateQueueWorkers(self):
        self.processWidget.setWindowTitle('Process Queue: (' +str(self.processList.count()) + ' items)')
        if(self.activeWorkers): # This is to counteract some weird case of the list being [None] when empty
            for worker in self.activeWorkers: # Checking if any of the workers have returned
                worker.updateJobWidget()
                if(worker.killRequest == True):
                    self.terminateRunningJob(worker)
                elif(self.pollThreadForCompletion(worker) == False):
                    self.completeJob(worker)

        if(len(self.activeWorkers) < self.numWorkers):
            #if(self.jobQueue.empty() is False):
            if(self.processList.count() is not 0):
                newWorker = self.startNextWorker()
                if(newWorker):
                    self.activeWorkers.append(newWorker)

    def pollThreadForCompletion(self, worker):
        return worker.process.is_alive()

    def abortJob(self, worker):
        if(worker.jobActive == False):
            worker.removeJobWidget(self.processList)
        else:
            worker.killSelf()

    def terminateRunningJob(self, worker):
        worker.removeJobWidget(self.processList)
        worker.releaseMgr()
        self.activeWorkers.remove(worker)

    def completeJob(self, worker):
        Op = self.workspace.submitOperation(worker.uScript, worker.selectedItem)
        dataOut = worker.dOut
        idx = 0
        for dataSet in dataOut:
            if(dataSet.verify()):
                dataSet.name = self.workspace.cleanStringName(dataSet.name)
                self.workspace.submitResultsToWorkspace(Op, dataSet)
            else:
                print('DataSet[' + str(idx) + '] is corrupted: Aborting Import.')
            idx += 1

        worker.removeJobWidget(self.processList)
        worker.releaseMgr()
        self.activeWorkers.remove(worker)

    def submitJob(self, script, selectedItem):
        self.createJobForQueue(script, selectedItem)

class userScriptsController():
    scripts = {'Display': [], 'Export': [], 'Generator': [], 'Import': [], 'Interact': [], 'Operation': []}
    uScriptDir = ''
    parent = []

    def __init__(self, dir, parent):
        self.uScriptDir = dir
        self.parent = parent
        self.getUserScripts()
        self.processManager = scriptProcessManager(parent)

    def getUserScripts(self):
        self.scripts['Display'] = self.getUserScriptsByType(UserDisplay)
        self.scripts['Export'] = self.getUserScriptsByType(UserExport)
        self.scripts['Generator'] = self.getUserScriptsByType(UserGenerator)
        self.scripts['Import'] = self.getUserScriptsByType(UserImport)
        self.scripts['Interact'] = self.getUserScriptsByType(UserInteract)
        self.scripts['Operation'] = self.getUserScriptsByType(UserOperation)

        self.parseImportScripts()

    def getImporterByExt(self, ext):
        ext = ext.upper()
        if ext in self.parent.settings['Default Importers']:
            defImporterName = self.parent.settings['Default Importers'][ext]
            for importer in self.registeredImportersList[ext]:
                if(importer.name == defImporterName):
                    return importer
            return None
        else:
            return None

    def runDefaultImporter(self, URL, ext):
        defImporter = self.getImporterByExt(ext)
        if(defImporter is not None):
            self.doImport(URL, ext, defImporter)
        else:
            print('No import function for extension: ' + ext)

    def runImporter(self, importer):
        fname = QFileDialog.getOpenFileNames(self.parent.mainWindow, 'Open File', self.parent.workspaceURL, filter=importer.genFilter())
        for fileURL in fname[0]:
            fileName, fileExtension = os.path.splitext(fileURL)
            self.doImport(fileURL, fileExtension, importer)

    def doImport(self, URL, ext, importer):
        print('Importing (' + URL +') using [' + importer.name + ']...')
        fileName = os.path.basename(URL)
        DataOut = []
        try:
            result = importer.import_func(DataOut, URL, fileName)
        except:
            print('Exception raised when importing using ' + importer.name + '. Aborting import.')
            result = False
        if(result):
            for DataSet in DataOut:
                if(DataSet.verify()):
                    if(DataSet.name == ''):
                        DataSet.name = fileName
                    DataSet.name = self.parent.cleanStringName(DataSet.name)
                    self.parent.submitResultsToWorkspace(None, DataSet)
                else:
                    print('DataSet is corrupted: Aborting Import.')
        else:
            print('Import Error!')

    def genImportDialogFilter(self):
        outputList = ''
        for key, val in sorted(self.registeredImportersList.items()):
            outputList = outputList + '*' + key.lower() + ';;'
        return outputList

    def parseImportScripts(self):
        self.registeredImportersList = {}
        for script in self.scripts['Import']:
            for key, ext in script.registeredFiletypes.items():
                ext = ext.upper()
                if ext in self.registeredImportersList:
                    self.registeredImportersList[ext].append(script)
                else:
                    self.registeredImportersList[ext] = [script]

        for ext in self.registeredImportersList:
            if ext in self.parent.settings['Default Importers']:
                stillExists = False
                for importer in self.registeredImportersList[ext]:
                    if(importer.name == self.parent.settings['Default Importers'][ext]):
                        stillExists = True

                if(stillExists == False):
                    print('Default Importer for ' + ext + ' no longer exists.')
                    self.parent.settings['Default Importers'][ext] = self.registeredImportersList[ext][0].name
            else:
                self.parent.settings['Default Importers'][ext] = self.registeredImportersList[ext][0].name

        self.parent.updateSettings()

    def loadUserScriptFromFile(self, filepath, scriptType):
        class_inst = None
        expected_class = 'ds_user_script'
        py_mod = None

        mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)

        if (py_mod != None):
            if hasattr(py_mod, expected_class):  # verify that ds_user_script is a class in this file
                class_temp = getattr(py_mod, expected_class)(filepath)
                if isinstance(class_temp, scriptType):  # verify that ds_user_script inherits the correct class
                    class_inst = class_temp

        return class_inst

    def initActionForScript(self, script, mW, selectedItem):
        action = QAction(QIcon('icons4\settings-6.png'), script.name, mW)
        action.setStatusTip(script.tooltip)
        action.triggered.connect(lambda: self.processManager.submitJob(script, selectedItem))
        return action

    def populateActionMenu(self, menu, scriptType, mW, selectedItem):
        for script in self.scripts[scriptType.type]:
            action = self.initActionForScript(script, mW, selectedItem)
            menu.addAction(action)

    def populateImportMenu(self, menu, mW):
        for script in self.scripts['Import']:
            action = QAction(QIcon('icons2\pendrive.png'), script.name, mW)
            action.setStatusTip('Import file(s) with ' + script.name)
            action.triggered.connect(functools.partial(self.runImporter, script))
            menu.addAction(action)

    def printUserScriptNames(self):
        for sType in self.scripts.items():
            for script in sType[1]:
                script.printName()

    def printUserScriptURLs(self):
        for sType in self.scripts.items():
            for script in sType[1]:
                script.printURL()

    def getUserScriptNamesByType(self, scriptType):
        nameList = []
        for script in self.scripts[scriptType.type]:
            nameList.append(script.name)
        return sorted(nameList)

    def getUserScriptsByType(self, scriptType):
        userScriptsOut = []
        typeScriptDir = os.path.join(self.uScriptDir, scriptType.type)

        for root, dirs, files in os.walk(typeScriptDir):
            for name in files:
                url = os.path.join(root, name)
                scriptHolder = self.loadUserScriptFromFile(url, scriptType)
                if (scriptHolder != None):
                    userScriptsOut.append(scriptHolder)

        return userScriptsOut