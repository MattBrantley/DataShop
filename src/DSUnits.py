#----------------------------------------------- UNITS ----------------------------------------------------------------#

class DSUnits():
    baseQuantity = 'Arbitrary'
    baseUnit = 'arbitrary units'
    baseUnitSymbol = 'arb'
    derived = False

class arbitrary(DSUnits):
    baseQuantity = 'arbitrary'
    baseUnit = 'arb units'
    baseUnitSymbol = 'arb'
    derived = False

class meter(DSUnits):
    baseQuantity = 'length'
    baseUnit = 'meter'
    baseUnitSymbol = 'm'
    derived = False

class gram(DSUnits):
    baseQuantity = 'mass'
    baseUnit = 'gram'
    baseUnitSymbol = 'g'
    derived = False

class seconds(DSUnits):
    baseQuantity = 'time'
    baseUnit = 'second'
    baseUnitSymbol = 's'
    derived = False

class ampere(DSUnits):
    baseQuantity = 'electric current'
    baseUnit = 'ampere'
    baseUnitSymbol = 'A'
    derived = False

class kelvin(DSUnits):
    baseQuantity = 'thermodynamic temperature'
    baseUnit = 'kelvin'
    baseUnitSymbol = 'K'
    derived = False