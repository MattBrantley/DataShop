from UserScript import UserOperation, ScriptIOData
from time import sleep

class ds_user_script(UserOperation):
    name = 'Locked Thread'
    tooltip = 'Runs for 1 second then simulates a locked thread.'
    nDimension = 2
    nDataSets = 1

    def operation(self, DataOut, DataIn, Meta):

        for num in range(0, 10):
            Meta['Progress'] = num
            sleep(.100)

        while(True):
            1+1

        outputData = ScriptIOData()
        outputData.matrix = DataIn[0].matrix
        DataOut.append(outputData)