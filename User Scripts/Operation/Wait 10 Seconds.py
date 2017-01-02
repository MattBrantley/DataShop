from UserScript import *
from time import sleep

class ds_user_script(UserOperation):
    name = 'Wait X Seconds'
    tooltip = 'Waits for a variable seconds and returns the input matrix'

    LengthSetting = IntegerSettingsObject(minimum=1, maximum=30, default=5)
    OtherSettingInt = IntegerSettingsObject(minimum=-500, maximum=500, default=100)
    SelectionSetting = RingSettingsObject()
    Opt1 = SelectionSetting.addSelection('Option 1')
    Opt2 = SelectionSetting.addSelection('Option 2')
    Opt3 = SelectionSetting.addSelection('Option 3')
    SelectionSetting.setDefault(Opt3)
    FloatSelection = FloatSettingsObject(maximum=7.2, default=-1.2)
    BoolSelection = BoolSettingsObject(default=True)
    StringSelection = StringSettingsObject(default='A String!')

    DataSetSelection = DataSetSettingsObject(minimum=3, maximum=4)
    PrimarySelection = DataSetSettingsObject(maximum=4, primaryEnabled=True)
    DataSetSelection.setDescription('Data sets to be output after sleep.')

    settings = {'Length': LengthSetting,
                'Other-Integer': OtherSettingInt,
                'Combo': SelectionSetting,
                'Float': FloatSelection,
                'Bool': BoolSelection,
                'Data': DataSetSelection,
                'Data2': PrimarySelection,
                'String': StringSelection}

    def operation(self, DataOut, Meta):
        print('Waiting for ' + str(Meta['Length']) + ' seconds..')
        print('Other-Integer setting =  ' + str(Meta['Other-Integer']))
        print('Combo selection = ' + Meta['Combo'])
        print('Float selection = ' + str(Meta['Float']))
        print('Bool selection = ' + str(Meta['Bool']))
        print('String selection = ' + str(Meta['String']))
        print('Primary selection name = ' + Meta['Data2'][0].name)

        if(Meta['Combo'] == 'Option 1'):
            print('YOU SELECTED NUMBER ! DOOD')

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