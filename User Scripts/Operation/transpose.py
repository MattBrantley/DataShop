from UserScript import UserOperation, ScriptIOData

class ds_user_script(UserOperation):
    name = 'Transpose'
    tooltip = 'Transpose the data matrix'
    nDimension = 2
    nDataSets = 1

    def operation(self):
        outputData = ScriptIOData()
        outputData.matrix = self.DataIn[0].matrix-100
        self.DataOut.append(outputData)
