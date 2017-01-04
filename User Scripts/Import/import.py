from UserScript import *

class ds_user_script(UserImport):
    name = 'CSV Importer 2D'
    registeredFiletypes = {'Column Separated CSV': '.csv', 'Something Else': '.SomethingElse'}

    def import_func(self, DataOut, URL, FileName):
        try:
            loadedData = np.genfromtxt(URL, delimiter=',')
            #print(type(loadedData))
            #print(loadedData.shape)
            axisData = loadedData[:,0]
            matrixData = loadedData[:,1]

            outputData = ScriptIOData()
            outputData.matrix = matrixData
            outputData.name = FileName

            axisObject = ScriptIOAxis()
            axisObject.name = 'Example Axis'
            axisObject.vector = axisData

            outputData.axes.append(axisObject)

            DataOut.append(outputData)

            return True
        except ValueError:
            print('Import Error, .csv might be corrupted.')
            return False

