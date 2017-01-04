from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QVariant, QTimer, QSize

class DataViewerWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.show()

        self.workspace = QDockWidget("No Workspace Loaded", self)
        self.workspace.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.workspace.setWidget(QWidget())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.workspace)