from UserScript import UserOperation, ScriptIOData
from time import sleep

class ds_user_script(UserOperation):
    name = 'Wait 5 Seconds'
    tooltip = 'Waits 5 seconds and returns the input matrix'
    nDimension = 2
    nDataSets = 1

    def operation(self, DataOut, DataIn):
        outputData = ScriptIOData()
        sleep(5)
        outputData.matrix = DataIn[0].matrix
        DataOut.append(outputData)