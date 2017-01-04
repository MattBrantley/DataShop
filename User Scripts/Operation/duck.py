# -*- coding: utf-8 -*-
"""
Duck.
"""

from UserScript import *
import matplotlib.pyplot as quackquack
import matplotlib as ducker
import os as quack
import random as featherbottom

class ds_user_script(UserOperation):
    """Duck."""

    name = 'Duck'
    tooltip = 'Quack'
    nDimension = 'Duck'
    nDataSets = 'Duck'
    version = 'Duck'
    Duck = 'Duck'
    Quack = 'Quack'

    duck = DataSetSettingsObject()
    duck.setDescription('Duck')
    settings = {'Duck': duck}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        duckNest = quack.path.dirname(quack.path.realpath(__file__))
        whereDucks = '{}\\functions\\ducks\\'.format(duckNest)
        'Quack Quack'
        ducks = [duck for duck in quack.listdir(whereDucks)]
        thatDuck = featherbottom.choice(ducks)
        hereDucky = whereDucks + thatDuck
        'Quack'
        duck = ducker.image.imread(hereDucky)
        quackquack.imshow(duck)
        quackquack.show()
