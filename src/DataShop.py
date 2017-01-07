import sys, uuid, pickle, numpy as np, sqlite3, os, matplotlib.pyplot as plt, random, psutil, imp, multiprocessing, copy, queue, json, DSUnits
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
from PyQt5.QtGui import *
from UserScriptsController import *
from UserScript import *

import DSUnits, DSPrefix
from DSWorkspace import DSWorkspace
from DSWidgets.settingsWidget import settingsDockWidget, settingsDefaultImporterListWidget
from DSWidgets.inspectorWidget import inspectorDockWidget
from DSWidgets.workspaceWidget import workspaceTreeDockWidget, WorkspaceTreeWidget

sys._excepthook = sys.excepthook

def default_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = default_exception_hook

class mainWindow(QMainWindow):
    MW_STATE_NO_WORKSPACE = 0
    MW_STATE_WORKSPACE_LOADED = 1

    def __init__(self):
        super().__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.statusBar()

        self.workspace = DSWorkspace(self)

        self.workspaceTreeDockWidget = workspaceTreeDockWidget(self)
        self.settingsDockWidget = settingsDockWidget(self)
        self.inspectorDockWidget = inspectorDockWidget(self)

        self.workspace.workspaceTreeWidget = self.workspaceTreeDockWidget.workspaceTreeWidget

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
            self.importMenu.setEnabled(False)
            self.workspaceTreeDockWidget.workspaceTreeWidget.setAcceptDrops(False)
        elif(state == self.MW_STATE_WORKSPACE_LOADED):
            self.exitAction.setEnabled(True)
            self.newAction.setEnabled(True)
            self.saveAction.setEnabled(True)
            self.openAction.setEnabled(True)
            self.settingsAction.setEnabled(False)
            self.importAction.setEnabled(True)
            self.importMenu.setEnabled(True)
            self.workspaceTreeDockWidget.workspaceTreeWidget.setAcceptDrops(True)
        else:
            self.exitAction.setEnabled(False)
            self.newAction.setEnabled(False)
            self.saveAction.setEnabled(False)
            self.openAction.setEnabled(False)
            self.settingsAction.setEnabled(False)
            self.importAction.setEnabled(False)
            self.importMenu.setEnabled(False)
            self.workspaceTreeDockWidget.workspaceTreeWidget.setAcceptDrops(False)

    def initActions(self):
        self.exitAction = QAction(QIcon('icons2\minimize.png'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit Application')
        self.exitAction.triggered.connect(self.close)

        self.newAction = QAction(QIcon('icons2\controller.png'), 'New Workspace', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('Create a New Workspace')
        self.newAction.triggered.connect(self.workspace.newWorkspace)

        self.saveAction = QAction(QIcon('icons2\save.png'), 'Save Workspace As..', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save Workspace As..')
        self.saveAction.triggered.connect(self.workspace.saveWSToNewSql)

        self.openAction = QAction(QIcon('icons2\\folder.png'), 'Open Workspace', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open Workspace')
        self.openAction.triggered.connect(self.workspace.loadWSFromSql)

        self.settingsAction = QAction(QIcon('icons2\settings.png'), 'Settings', self)
        self.settingsAction.setShortcut('Ctrl+S')
        self.settingsAction.setStatusTip('Adjust Settings')

        self.importAction = QAction(QIcon('icons2\pendrive.png'), 'Import', self)
        self.importAction.setStatusTip('Import Data')
        self.importAction.triggered.connect(self.workspace.importData)

        self.viewWindowsAction = QAction('Import', self)
        self.viewWindowsAction.triggered.connect(self.populateViewWindowMenu)

    def initUI(self):
        self.initMenu()
        self.initToolbar()
        self.updateState(self.MW_STATE_NO_WORKSPACE)

        self.centralWidget.setAutoFillBackground(True)
        pal = self.centralWidget.palette()
        pal.setColor(self.centralWidget.backgroundRole(), Qt.white)
        self.centralWidget.setPalette(pal)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.workspaceTreeDockWidget)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.settingsDockWidget)
        self.settingsDockWidget.setFloating(True)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.inspectorDockWidget)
        self.inspectorDockWidget.setFloating(True)

        self.AnimatedDocks = True
        self.setDockNestingEnabled(True)

        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('DataShop (Alpha)')
        self.show()

    def populateViewWindowMenu(self):
        windows = self.findChildren(QDockWidget)
        self.viewWindowsMenu.clear()
        for window in windows:
            action = QAction(str(window.windowTitle()), self)
            action.setCheckable(True)
            action.setChecked(window.isVisible())
            #self.workspace.to
            if(window.isVisible()):
                action.triggered.connect(window.hide)
            else:
                action.triggered.connect(window.show)

            self.viewWindowsMenu.addAction(action)

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

        self.viewWindowsMenu = QMenu('Windows')
        self.viewWindowsMenu.aboutToShow.connect(self.populateViewWindowMenu)

        self.viewMenu = self.menubar.addMenu('&View')
        self.viewMenu.addMenu(self.viewWindowsMenu)

        self.importMenu = self.menubar.addMenu('&Import')
        self.workspace.userScripts.populateImportMenu(self.importMenu, self)

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
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
