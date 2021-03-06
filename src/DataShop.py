import sys, uuid, pickle, numpy as np, sqlite3, os, matplotlib.pyplot as plt, random, psutil, imp, multiprocessing, copy, queue
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from xml.dom.minidom import *
from xml.etree.ElementTree import *
from PyQt5.QtCore import Qt, QVariant, QTimer, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from UserScriptsController import *
from UserScript import *

class WorkspaceTree(QTreeWidget):

    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)

class DSWorkspace():
    workspaceURL = ''
    directoryURL = os.path.dirname(os.path.realpath(__file__))
    userScripts = None
    ITEM_GUID = Qt.UserRole
    ITEM_TYPE = Qt.UserRole+1
    ITEM_NAME = Qt.UserRole+2

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.initTree()

    def initTree(self):
        self.treeWidget = WorkspaceTree()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)

        self.buildUserScripts()

        self.root = self.treeWidget.invisibleRootItem()

    def buildUserScripts(self):
        scriptsURL = os.path.join(str(Path(self.directoryURL).parent), 'User Scripts')
        self.userScripts = userScriptsController(scriptsURL, self)

    def setLoadedWorkspace(self, URL):
        self.workspaceURL = URL
        self.directoryURL = os.path.dirname(URL)
        mW.workspace.setWindowTitle(os.path.basename(URL))
        mW.updateState(mW.MW_STATE_WORKSPACE_LOADED)

    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        j = "\n" + (level - 1) * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem

    def toXML(self):
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        workingInd = []
        wsXML = Element('Workspace')
        wsXML.append(Comment('Workspace Variables and Operators are Contained Here'))
        while iterator.value():
            item = iterator.value()
            level = self.getItemLevel(item)
            if(len(workingInd) <= level):
                workingInd.append(0)
            if(level > 0):
                workingInd[level] = SubElement(workingInd[level-1], item.data(0, self.ITEM_TYPE))
            else:
                workingInd[level] = SubElement(wsXML, item.data(0, self.ITEM_TYPE))
            workingInd[level].set('Name', item.data(0, self.ITEM_NAME))
            workingInd[level].set('GUID', item.data(0, self.ITEM_GUID))
            workingInd[level].set('Type', item.data(0, self.ITEM_TYPE))
            workingInd[level].text = "\n"
            workingInd[level].tail = "\n"
            iterator+=1
        return wsXML

    def fromXML(self, wsXMLString):
        self.treeWidget.clear()
        wsXML = XML(wsXMLString)
        self.treeItemFromXMLItem(wsXML, self.root)

    def treeItemFromXMLItem(self, xmlItem, treeItem):
        for child in xmlItem:
            Metadata = child.attrib
            nTreeItem = self.addItem(treeItem, Metadata)
            self.treeItemFromXMLItem(child, nTreeItem)

    def newWorkspace(self):
        fname = QFileDialog.getSaveFileName(mW, 'Save File', self.directoryURL, filter='*.db')
        if fname[0]:
            self.treeWidget.clear()
            xmlString = tostring(self.toXML(), encoding="unicode")
            self.setLoadedWorkspace(fname[0])
            conn = sqlite3.connect(fname[0])
            c = conn.cursor()
            c.execute('DROP TABLE IF EXISTS Workspace')
            c.execute('CREATE TABLE Workspace (bWorkspace TEXT NOT NULL, timeStamp date);')
            c.execute("INSERT INTO Workspace (bWorkspace, timeStamp) VALUES (?, CURRENT_TIMESTAMP);", (xmlString, )) #memoryview()
            conn.commit()
            conn.close()

    def saveWSToNewSql(self):
        fname = QFileDialog.getSaveFileName(mW, 'Save File', self.directoryURL)
        if fname[0]:
            self.setLoadedWorkspace(fname[0])
            self.saveWSToSql()

    def saveWSToSql(self):
        xmlString = tostring(self.toXML(), encoding="unicode")
        conn = sqlite3.connect(self.workspaceURL)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS Workspace')
        c.execute('CREATE TABLE Workspace (bWorkspace TEXT NOT NULL, timeStamp date);')
        c.execute("INSERT INTO Workspace (bWorkspace, timeStamp) VALUES (?, CURRENT_TIMESTAMP);", (xmlString, )) #memoryview()
        conn.commit()
        conn.close()

    def saveDSToSql(self, name, data):
        GUID = str(uuid.uuid4().hex)
        GUID = GUID.upper()
        conn = sqlite3.connect(self.workspaceURL)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS DataSets (Key INTEGER PRIMARY KEY ASC, Name TEXT NOT NULL, Data Blob, GUID TEXT, timeStamp date);')
        c.execute("INSERT INTO DataSets (Key, Name, Data, GUID, timeStamp) VALUES (NULL, ?, ?, ?, CURRENT_TIMESTAMP);", (name, data.dumps(), GUID)) #memoryview()
        #print(c.lastrowid)
        conn.commit()
        conn.close()
        return GUID

    def deleteDSFromSql(self, selectedItem):
        conn = sqlite3.connect(self.workspaceURL)
        c = conn.cursor()
        GUID = selectedItem.data(0, self.ITEM_GUID)
        c.execute('DELETE FROM DataSets WHERE GUID=?', (GUID, ))
        conn.commit()
        conn.close()

    def renameDSFromSql(self, selectedItem):
        conn = sqlite3.connect(self.workspaceURL)
        c = conn.cursor()
        GUID = selectedItem.data(0, self.ITEM_GUID)
        c.execute('UPDATE DataSets SET Name = ? WHERE GUID=?', (selectedItem.text(0), GUID, ))
        conn.commit()
        conn.close()

    def loadWSFromSql(self):
        fname = QFileDialog.getOpenFileName(mW, 'Open File', self.directoryURL, filter='*.db')
        if fname[0]:
            self.setLoadedWorkspace(fname[0])
            conn = sqlite3.connect(fname[0])
            c = conn.cursor()
            c.execute('SELECT bWorkspace, timeStamp FROM Workspace;')
            results = c.fetchone()
            bWorkspace = results[0]
            timeStamp = results[1]
            self.fromXML(bWorkspace)
            conn.commit()
            conn.close()

    def getItemLevel(self, item):
        level = 0
        while(item.parent()):
            level += 1
            item = item.parent()
        return level

    def addItem(self, parent, data):
        item = QTreeWidgetItem(parent)
        nName = data['Name']
        item.setText(0, nName)
        item.setData(0, self.ITEM_NAME, data['Name'])
        item.setData(0, self.ITEM_GUID, data['GUID'])
        item.setData(0, self.ITEM_TYPE, data['Type'])
        if(data['Type'] == 'Data'):
            item.setIcon(0, QIcon('icons4\database-1.png'))
        if(data['Type'] == 'Operation'):
            item.setIcon(0, QIcon('icons4\settings-6.png'))
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)
        #item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

        return item

    def cleanStringName(self, str):
        str = str.replace(" ", "_")
        return str

    def importData(self):
        #process = psutil.Process(os.getpid())
        #print(process.memory_info().rss)
        fname = QFileDialog.getOpenFileName(mW, 'Open File', self.workspaceURL, filter='*.csv')
        if fname[0]:
            try:
                data = np.genfromtxt(fname[0], delimiter=',')
                name = self.cleanStringName(os.path.basename(fname[0]))
                data = {'GUID': self.saveDSToSql(name, data), 'Type': 'Data', 'Name': name}
                self.addItem(self.root, data)
                self.saveWSToSql()
            except ValueError:
                print('Import Error, .csv might be corrupted.')

    def getItemData(self, selectedItem):
        GUID = selectedItem.data(0, self.ITEM_GUID)
        return self.loadDataByGUID(GUID)

    def loadDataByGUID(self, GUID):
        conn = sqlite3.connect(self.workspaceURL)
        c = conn.cursor()
        c.execute('SELECT Data FROM DataSets WHERE GUID=?', (GUID, ))
        results = c.fetchone()
        conn.commit()
        conn.close()
        data = None
        if(results):
            data = np.loads(results[0])
        return data

    def surfacePlotItem(self, selectedItem):
        dockWidget = QDockWidget(selectedItem.text(0), mW)
        multiWidget = QWidget()
        layout = QGridLayout()
        pltFigure = plt.figure()
        pltCanvas = FigureCanvas(pltFigure)
        pltToolbar = NavigationToolbar(pltCanvas, dockWidget)
        layout.addWidget(pltToolbar)
        layout.addWidget(pltCanvas)
        multiWidget.setLayout(layout)
        dockWidget.setWidget(multiWidget)
        dockWidget.setAttribute(Qt.WA_DeleteOnClose)
        mW.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setFloating(True)
        data = self.getItemData(selectedItem)
        ax = pltFigure.add_subplot(111, projection='3d')

        if isinstance(data, np.ndarray):
            if len(data.shape) == 2:
                row, col = data.shape
                xValues = np.arange(row)
                yValues = np.arange(col)
                x, y = np.meshgrid(xValues, yValues)
                ax.set_zlim(np.min(data), np.max(data))
                ax.set_xlim(np.min(xValues), np.max(xValues))
                ax.set_ylim(np.min(yValues), np.max(yValues))
                ax.view_init(elev=45, azim=45)
                ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 1.0))
                ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 1.0))
                ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 1.0))
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_zticks([])
                try:
                    ax.plot_surface(x, y, data.T, rstride=1, cstride=1000,
                                    cmap='GnBu', lw=0.1)
                except:
                    pass
            else:
                dockWidget.close()
        else:
            dockWidget.close()

    def linePlotItem(self, selectedItem):
        dockWidget = QDockWidget(selectedItem.text(0), mW)
        multiWidget = QWidget()
        layout = QGridLayout()
        pltFigure = plt.figure()
        pltCanvas = FigureCanvas(pltFigure)
        pltToolbar = NavigationToolbar(pltCanvas, dockWidget)
        layout.addWidget(pltToolbar)
        layout.addWidget(pltCanvas)
        multiWidget.setLayout(layout)
        dockWidget.setWidget(multiWidget)
        dockWidget.setAttribute(Qt.WA_DeleteOnClose)
        mW.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setFloating(True)

        data = self.getItemData(selectedItem)
        ax = pltFigure.add_subplot(111)
        if isinstance(data, np.ndarray):
            if len(data.shape) == 1:
                ax.plot(data)
            elif len(data.shape) == 2:
                row, col = data.shape
                if col == 1:
                    try:
                        ax.plot(data[:, 0])
                    except:
                        # Should add in a popup for the user to know that
                        # the argument was wrong, or some other feedback.
                        pass
                elif col == 2:
                    try:
                        ax.plot(data[:, 0], data[:, 1])
                    except:
                        pass
                elif row == 2:
                    try:
                        ax.plot(data[0], data[1])
                    except:
                        pass
                else:
                    dockWidget.close()
            else:
                dockWidget.close()
        else:
            dockWidget.close()

    def deleteItem(self, selectedItem):
        if(self.treeWidget.indexOfTopLevelItem(selectedItem) == -1): #Item is a child
            p = selectedItem.parent()
            p.removeChild(selectedItem)
        else:   #Item is top level (these are handled differently)
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(selectedItem))
        self.deleteDSFromSql(selectedItem)
        self.saveWSToSql()

    def renameItem(self, selectedItem):
        text, ok = QInputDialog.getText(mW, 'Rename Item', 'Enter New Name', text=selectedItem.text(0))
        if(ok):
            selectedItem.setText(0, self.cleanStringName(text))
            self.renameDSFromSql(selectedItem)
            self.saveWSToSql()

    def submitOperation(self, script, selectedItem):
        dataOp = {'GUID': '', 'Type': 'Operation', 'Name': 'Operation: ' + script.name}
        return self.addItem(selectedItem, dataOp)

    def submitResult(self, Op, dataSet):
        dataRes = {'GUID': self.saveDSToSql('Result', dataSet.matrix), 'Type': 'Data', 'Name': self.cleanStringName(dataSet.name)}
        self.addItem(Op, dataRes)
        self.saveWSToSql()

    def initContextActions(self, selectedItem):
        self.renameAction = QAction(QIcon('icons\\analytics-1.png'), 'Rename Item', mW)
        self.renameAction.setStatusTip('Rename this Item')
        self.renameAction.triggered.connect(lambda: self.renameItem(selectedItem))

        self.deleteAction = QAction(QIcon('icons\\transfer-1.png'),'Delete Item', mW)
        self.deleteAction.setStatusTip('Delete this Item from Memory')
        self.deleteAction.triggered.connect(lambda: self.deleteItem(selectedItem))

        self.linePlotAction = QAction(QIcon('icons\\analytics-4.png'),'Line Plot', mW)
        self.linePlotAction.setStatusTip('Generate a line plot of this DataSet')
        self.linePlotAction.triggered.connect(lambda: self.linePlotItem(selectedItem))

        self.surfacePlotAction = QAction(QIcon('icons\\analytics-4.png'),'Surface Plot', mW)
        self.surfacePlotAction.setStatusTip('Generate a surface plot of this DataSet')
        self.surfacePlotAction.triggered.connect(lambda: self.surfacePlotItem(selectedItem))

    def initContextMenu(self):
        selectedItem = self.treeWidget.currentItem()
        itemType = selectedItem.data(0, self.ITEM_TYPE)
        self.initContextActions(selectedItem)
        self.contextMenu = QMenu()

        #Universal Workspace Context Menu Actions
        if(self.userScripts.processManager.processList.count() is not 0):
            self.renameAction.setEnabled(False)
            self.deleteAction.setEnabled(False)
        self.contextMenu.addAction(self.renameAction)
        self.contextMenu.addAction(self.deleteAction)
        self.contextMenu.addSeparator()

        #Type Specific Context Menu Actions
        if(itemType == 'Data'):
            self.contextMenu.addAction(self.linePlotAction)
            self.contextMenu.addAction(self.surfacePlotAction)
            self.contextMenu.addSeparator()
            self.userScripts.populateActionMenu(self.contextMenu.addMenu('Operations'), UserOperation, mW, selectedItem)

        #elif(itemType == 'Operation'):

    def initDefaultContextMenu(self):
        warningAction = QAction('Nothing selected!', mW)
        warningAction.setStatusTip('Nothing has been selected!')
        warningAction.setEnabled(False)

        self.contextMenu = QMenu()
        self.contextMenu.addAction(warningAction)

    def openMenu(self, position):
        if(self.treeWidget.selectedItems()):
            self.initContextMenu()
            self.contextMenu.exec_(self.treeWidget.viewport().mapToGlobal(position))
        else:
            self.initDefaultContextMenu()
            self.contextMenu.exec_(self.treeWidget.viewport().mapToGlobal(position))

    def getTreeWidget(self):
        return self.treeWidget

class mainWindow(QMainWindow):
    MW_STATE_NO_WORKSPACE = 0
    MW_STATE_WORKSPACE_LOADED = 1

    def __init__(self):
        super().__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.treeHolder = DSWorkspace(self)
        self.statusBar()
        self.workspace = QDockWidget("No Workspace Loaded", self)

        self.initActions()
        self.initUI()

    def updateState(self, state):
        if(state == self.MW_STATE_NO_WORKSPACE):
            self.exitAction.setEnabled(True)
            self.newAction.setEnabled(True)
            self.saveAction.setEnabled(False)
            self.openAction.setEnabled(True)
            self.settingsAction.setEnabled(False)
            self.importAction.setEnabled(False)
        elif(state == self.MW_STATE_WORKSPACE_LOADED):
            self.exitAction.setEnabled(True)
            self.newAction.setEnabled(True)
            self.saveAction.setEnabled(True)
            self.openAction.setEnabled(True)
            self.settingsAction.setEnabled(False)
            self.importAction.setEnabled(True)
        else:
            self.exitAction.setEnabled(False)
            self.newAction.setEnabled(False)
            self.saveAction.setEnabled(False)
            self.openAction.setEnabled(False)
            self.settingsAction.setEnabled(False)
            self.importAction.setEnabled(False)

    def initActions(self):
        self.exitAction = QAction(QIcon('icons2\minimize.png'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit Application')
        self.exitAction.triggered.connect(self.close)

        self.newAction = QAction(QIcon('icons2\controller.png'), 'New Workspace', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('Create a New Workspace')
        self.newAction.triggered.connect(self.treeHolder.newWorkspace)

        self.saveAction = QAction(QIcon('icons2\save.png'), 'Save Workspace As..', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save Workspace As..')
        self.saveAction.triggered.connect(self.treeHolder.saveWSToNewSql)

        self.openAction = QAction(QIcon('icons2\\folder.png'), 'Open Workspace', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open Workspace')
        self.openAction.triggered.connect(self.treeHolder.loadWSFromSql)

        self.settingsAction = QAction(QIcon('icons2\settings.png'), 'Settings', self)
        self.settingsAction.setShortcut('Ctrl+S')
        self.settingsAction.setStatusTip('Adjust Settings')

        self.importAction = QAction(QIcon('icons2\pendrive.png'), 'Import', self)
        self.importAction.setStatusTip('Import Data')
        self.importAction.triggered.connect(self.treeHolder.importData)

    def initUI(self):
        self.initMenu()
        self.initToolbar()
        self.updateState(self.MW_STATE_NO_WORKSPACE)

        self.centralWidget.setAutoFillBackground(True)
        pal = self.centralWidget.palette()
        pal.setColor(self.centralWidget.backgroundRole(), Qt.white)
        self.centralWidget.setPalette(pal)

        self.workspace.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.workspace.setWidget(self.treeHolder.getTreeWidget())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.workspace)

        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('DataShop (Alpha)')
        self.show()

    def initMenu(self):
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.settingsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

    def initToolbar(self):
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.settingsAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.importAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.exitAction)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mW = mainWindow()
    sys.exit(app.exec_())
