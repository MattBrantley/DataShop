#----------------------------------------------- UNITS ----------------------------------------------------------------#

class DSUnits():
    baseQuantity = 'Arbitrary'
    baseUnit = 'arbitrary units'
    baseUnitSymbol = 'arb'
    baseUnit = True

    def __init__(self):
        print('Initiliazing DSUnits..')

class arbitrary(DSUnits):
    baseQuantity = 'arbitrary'
    baseUnit = 'arb units'
    baseUnitSymbol = 'arb'
    baseUnit = True

class meter(DSUnits):
    baseQuantity = 'length'
    baseUnit = 'meter'
    baseUnitSymbol = 'm'
    baseUnit = True

class gram(DSUnits):
    baseQuantity = 'mass'
    baseUnit = 'gram'
    baseUnitSymbol = 'g'
    baseUnit = True

class seconds(DSUnits):
    baseQuantity = 'time'
    baseUnit = 'second'
    baseUnitSymbol = 's'
    baseUnit = True

class ampere(DSUnits):
    baseQuantity = 'electric current'
    baseUnit = 'ampere'
    baseUnitSymbol = 'A'
    baseUnit = True

class kelvin(DSUnits):
    baseQuantity = 'thermodynamic temperature'
    baseUnit = 'kelvin'
    baseUnitSymbol = 'K'
    baseUnit = True