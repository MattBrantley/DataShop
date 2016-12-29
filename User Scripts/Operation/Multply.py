from UserScript import UserOperation, ScriptIOData

class ds_user_script(UserOperation):
    name = 'Multiply'
    tooltip = 'Multiply the data set by itself'
    nDimension = 2
    nDataSets = 1

    def operation(self):
        outputData = ScriptIOData()
        outputData.matrix = self.DataIn[0].matrix*self.DataIn[0].matrix
        self.DataOut.append(outputData)