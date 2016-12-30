from UserScript import UserOperation, ScriptIOData
from time import sleep

class ds_user_script(UserOperation):
    name = 'Wait 10 Seconds'
    tooltip = 'Waits 10 seconds and returns the input matrix'
    nDimension = 2
    nDataSets = 1

    def operation(self, DataOut, DataIn, Meta):

        for num in range(0, 100):
            Meta['Progress'] = num
            sleep(.100)
        outputData = ScriptIOData()
        outputData.matrix = DataIn[0].matrix
        DataOut.append(outputData)