from UserScript import *
from time import sleep

class ds_user_script(UserOperation):
    name = 'Wait X Seconds'
    tooltip = 'Waits for a variable seconds and returns the input matrix'

    LengthSetting = IntegerSettingsObject(minimum=1, maximum=30, default=5)
    OtherSetting = IntegerSettingsObject(minimum=-500, maximum=500, default=100)
    SelectionSetting = RingSettingsObject()
    Opt1 = SelectionSetting.addSelection('Option 1')
    Opt2 = SelectionSetting.addSelection('Option 2')
    Opt3 = SelectionSetting.addSelection('Option 3')
    SelectionSetting.setDefault(Opt3)
    FloatSelection = FloatSettingsObject(minimum=-4.5, maximum=7.2, default=-1.2)
    BoolSelection = BoolSettingsObject(default=True)

    DataSetSelection = DataSetSettingsObject(count=4)

    settings = {'Length': LengthSetting,
                'Other': OtherSetting,
                'Combo': SelectionSetting,
                'Float': FloatSelection,
                'Bool': BoolSelection,
                'Data': DataSetSelection}

    def operation(self, DataOut, Meta):
        print('Waiting for ' + str(Meta['Length']) + ' seconds..')
        print('Other setting =  ' + str(Meta['Other']))
        print('Combo selection = ' + Meta['Combo'])
        print('Float selection = ' + str(Meta['Float']))
        print('Bool selection = ' + str(Meta['Bool']))


        for num in range(0, 100):
            Meta['Progress'] = num
            sleep(Meta['Length']/100)

        idx = 0
        for item in Meta['Data']:
            idx += 1
            outputData = ScriptIOData()
            outputData.matrix = item.matrix
            outputData.name = str(Meta['Length']) + ' Second Wait (#' + str(idx) + ')'
            DataOut.append(outputData)