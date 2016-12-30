from UserScript import UserOperation, ScriptIOData

class ds_user_script(UserOperation):
    name = 'Multiply'
    tooltip = 'Multiply the data set by itself'
    nDimension = 2
    nDataSets = 1

    def operation(self, DataOut, DataIn):
        outputData = ScriptIOData()
        outputData.matrix = DataIn[0].matrix*DataIn[0].matrix
        DataOut.append(outputData)