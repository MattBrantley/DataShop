from UserScript import UserOperation, ScriptIOData

class ds_user_script(UserOperation):
    name = 'Invert'
    tooltip = 'Invert Sign of Dataset Elements'
    nDimension = 2
    nDataSets = 1

    def operation(self):
        outputData = ScriptIOData()
        outputData.matrix = self.DataIn[0].matrix*-1
        self.DataOut.append(outputData)