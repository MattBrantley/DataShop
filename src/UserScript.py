import numpy as np, sys, copy, collections
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
from UserScriptSettingsObjects import *
import DSUnits, DSPrefix

class ScriptIOAxis():

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'N/A')
        self.units = kwargs.get('units', DSUnits.arbitrary())
        self.prefix = kwargs.get('prefix', DSPrefix.noPrefix())
        self.length = 0
        tVector = kwargs.get('vector', None)
        if(tVector is not None):
            self.setVector(tVector)
        else:
            self.vector = None

    def setName(self, string):
        self.name = string

    def setVector(self, vector):
        if(issubclass(type(vector), np.ndarray)):
            if(len(vector.shape) is 1):
                self.vector = vector
                self.length = vector[0].size
            else:
                print('Axis vector cannot have more than 1 dimension')
        else:
            print('Axis vector must be of type numpy.ndarray')

    def setUnits(self, prefix, units):
        if(issubclass(type(prefix), DSPrefix)):
            self.prefix = prefix
        else:
            print('Invalid prefix being set.')

        if(isinstance(units, DSUnits)):
            self.units = units
        else:
            print('Invalid units being sets.')

class ScriptIOData():

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Result')
        self.units = kwargs.get('units', DSUnits.arbitrary())
        self.prefix = kwargs.get('prefix', DSPrefix.noPrefix())
        self.numDims = 0
        self.Op = None

        tMatrix = kwargs.get('matrix', None)
        if(tMatrix is not None):
            self.setMatrix(tMatrix)
        else:
            self.Matrix = None
        self.axes = []

    def setMatrix(self, matrix):
        if(issubclass(type(matrix), np.ndarray)):
            self.matrix = matrix
            self.numDims = len(self.matrix.shape)
        else:
            print('Matrix must be of type numpy.ndarray')

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
                print('Critical Error!: axis[' + str(axisIdx) + '].vector is of type (' + str(type(axis.vector)) + '). Axis must be of type numpy.ndarray. Data is corrupt, returning..')
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