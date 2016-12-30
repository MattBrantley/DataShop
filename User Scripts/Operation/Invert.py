from UserScript import UserOperation, ScriptIOData

class ds_user_script(UserOperation):
    """THIS IS A DOCSTRING FOR THE INVERT FUNCTION"""
    name = 'Invert'
    tooltip = 'Invert Sign of Dataset Elements'
    nDimension = 2
    nDataSets = 1

    def operation(self, DataOut, DataIn, Meta):
        outputData = ScriptIOData()
        outputData.matrix = DataIn[0].matrix*-1
        DataOut.append(outputData)