from UserScript import UserOperation, ScriptIOData

class ds_user_script(UserOperation):
    name = 'Clone - Invert'
    tooltip = 'Clone Dataset to Produce Two Identical (But Inverted) Datasets'
    nDimension = 2
    nDataSets = 1

    def operation(self):
        outputData1 = ScriptIOData()
        outputData2 = ScriptIOData()
        outputData1.matrix = self.DataIn[0].matrix*-1
        outputData2.matrix = self.DataIn[0].matrix
        self.DataOut.append(outputData1)
        self.DataOut.append(outputData2)