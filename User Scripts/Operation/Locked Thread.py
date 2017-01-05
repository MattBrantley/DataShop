from UserScript import *
from time import sleep

class ds_user_script(UserOperation):
    name = 'Locked Thread'
    tooltip = 'Runs for 1 second then simulates a locked thread.'

    PrimarySelection = DataSetSettingsObject(maximum=4, primaryEnabled=True)


    settings = {'Data': PrimarySelection}

    def operation(self, DataOut, Meta):

        for num in range(0, 10):
            Meta['Progress'] = num
            sleep(.100)

        while(True):
            1+1

        #outputData = ScriptIOData()
        #outputData.matrix = DataIn[0].matrix
        #DataOut.append(outputData)