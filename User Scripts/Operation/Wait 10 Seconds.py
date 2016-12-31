from UserScript import *
from time import sleep

class ds_user_script(UserOperation):
    name = 'Wait X Seconds'
    tooltip = 'Waits for a variable seconds and returns the input matrix'
    nDimension = 2
    nDataSets = 1

    LengthSetting = IntegerSettingsObject(minimum=0, maximum=10, default=5)
    OtherSetting = IntegerSettingsObject(minimum=-500, maximum=500, default=100)
    SelectionSetting = RingSettingsObject()
    Opt1 = SelectionSetting.addSelection('Option 1')
    Opt2 = SelectionSetting.addSelection('Option 2')
    Opt3 = SelectionSetting.addSelection('Option 3')
    SelectionSetting.setDefault(Opt3)

    settings = {'Length': LengthSetting, 'Other': OtherSetting, 'Combo': SelectionSetting}
    #settings = {'Length': LengthSetting, 'Other': OtherSetting}

    def operation(self, DataOut, DataIn, Meta):
        print('Waiting for ' + str(Meta['Length']) + ' seconds..')
        print('Other setting =  ' + str(Meta['Other']))
        print('Combo selection = ' + Meta['Combo'])
        for num in range(0, 100):
            Meta['Progress'] = num
            sleep(Meta['Length']/100)
        outputData = ScriptIOData()
        outputData.matrix = DataIn[0].matrix
        outputData.name = str(Meta['Length']) + ' Second Wait'
        DataOut.append(outputData)