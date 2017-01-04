import numpy as np, sys, copy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
from UserScriptSettingsObjects import *

class ScriptIOData():
    matrix = []
    name = 'Result'

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
    registeredFiletypes = {}

    def import_func(self, DataOut, URL, FileName):
        print('Nothing was imported!')
        return False

    def genFilter(self):
        outputList = ''
        for key, val in sorted(self.registeredFiletypes.items()):
            outputList = outputList + '*' + val.lower() + ';;'
        return outputList[:-2]

class UserInteract(UserScript):
    type = 'Interact'

class UserOperation(UserScript):
    type = 'Operation'

    def start(self, dOut, meta, settings):
        self.settings = settings
        self.operation(dOut, meta)

    def operation(self, dOut, meta):
        print('Nothing Happened')