class DSPRefix():
    modifier = 1
    prefixText = ''
    prefixSymbol = ''

    def __init__(self):
        print('Initiliazing DSUnits..')

class noPrefix(DSPRefix):
    modifier = 1
    prefixText = ''
    prefixSymbol = ''

class deca(DSPRefix):
    modifier = 10E1
    prefixText = 'deca'
    prefixSymbol = 'da'

class hecto(DSPRefix):
    modifier = 10E2
    prefixText = 'hecto'
    prefixSymbol = 'h'

class kilo(DSPRefix):
    modifier = 10E3
    prefixText = 'kilo'
    prefixSymbol = 'k'

class mega(DSPRefix):
    modifier = 10E6
    prefixText = 'mega'
    prefixSymbol = 'M'

class giga(DSPRefix):
    modifier = 10E9
    prefixText = 'giga'
    prefixSymbol = 'G'

class tera(DSPRefix):
    modifier = 10E12
    prefixText = 'tera'
    prefixSymbol = 'T'

class peta(DSPRefix):
    modifier = 10E15
    prefixText = 'peta'
    prefixSymbol = 'P'

class exa(DSPRefix):
    modifier = 10E18
    prefixText = 'exa'
    prefixSymbol = 'E'

class deci(DSPRefix):
    modifier = 10E-1
    prefixText = 'deci'
    prefixSymbol = 'd'

class centi(DSPRefix):
    modifier = 10E-2
    prefixText = 'centi'
    prefixSymbol = 'c'

class milli(DSPRefix):
    modifier = 10E-3
    prefixText = 'milli'
    prefixSymbol = 'm'

class micro(DSPRefix):
    modifier = 10E-6
    prefixText = 'micro'
    prefixSymbol = 'u'

class nano(DSPRefix):
    modifier = 10E-9
    prefixText = 'nano'
    prefixSymbol = 'n'

class pico(DSPRefix):
    modifier = 10E-12
    prefixText = 'pico'
    prefixSymbol = 'p'

class femto(DSPRefix):
    modifier = 10E-15
    prefixText = 'femto'
    prefixSymbol = 'f'

class atto(DSPRefix):
    modifier = 10E-18
    prefixText = 'atto'
    prefixSymbol = 'a'