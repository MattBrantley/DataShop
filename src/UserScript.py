import numpy as np, sys, copy, collections
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
from UserScriptSettingsObjects import *

VALUE_CUSTOM_A = 1054

class ScriptIOAxis():
    name = 'N/A'
    units = 'arbitrary'
    length = 0
    vector = None

class ScriptIOData():

    def __init__(self):
        self.matrix = None
        self.axes = []
        self.name = 'Result'
        self.numDims = 0

    def verify(self): #Verifies the ScriptIODate is complete and valid
        #print('Verification Output:')
        if(type(self.matrix) is not np.ndarray):
            print('Critical Error!: matrix is of type (' + str(type(self.matrix)) + '). Matrix must be of type numpy.ndarray. Data is corrupt, returning..')
            return False

        if(type(self.axes) is not list):
            print('Critical Error!: axes is of type (' + str(type(self.axes)) + ') instead of list. Data is corrupt, returning..')
            return False

        if(len(self.axes) != len(self.matrix.shape)):
            print('Critical Error!: Number of axes (' + str(len(self.axes)) + ') does not match matrix dimension count (' + str(len(self.matrix.shape)) + '). Data is corrupt, returning..')
            return False

        axisIdx = 0
        for axis in self.axes:
            if(type(axis) is not ScriptIOAxis):
                print('Critical Error!: axis[' + str(axisIdx) + '] is of type (' + type(axis) + '), not of type ScriptIOAxis. Data is corrupt, returning..')
                return False

            if(type(axis.vector) is not np.ndarray):
                print('Critical Error!: axis[' + str(axisIdx) + '] is of type (' + str(type(axis.vector)) + '). Axis must be of type numpy.ndarray. Data is corrupt, returning..')
                return False

            if(len(axis.vector.shape) is not 1):
                print('Critical Error!: axis[' + str(axisIdx) + '] has ' + str(len(axis.vector.shape)) + ' dimensions but can only have 1. Data is corrupt, returning..')
                return False

            if(axis.vector.shape[0] != self.matrix.shape[axisIdx]):
                print('Critical Error!: axis[' + str(axisIdx) + '] does not match matrix dimension ' + str(axisIdx) + ' length (' + str(self.matrix.shape[axisIdx]) + '). Data is corrupt, returning..')
                return False
            axisIdx += 1

        if(self.numDims != len(self.axes)):
            #print('Warning: Dimension count (' + str(self.numDims) + ') does not match number of data axes (' + str(len(self.axes)) + '). Correcting...')
            self.numDims = len(self.axes)

        return True

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