from UserScript import *

class ds_user_script(UserImport):
    name = 'CSV Importer Type1'
    registeredFiletypes = {'Column Separated CSV': '.csv', 'Something Else': '.SomethingElse'}

    def import_func(self, DataOut, URL, FileName):
        try:
            outputData = ScriptIOData()
            outputData.matrix = np.genfromtxt(URL, delimiter=',')
            outputData.name = FileName
            DataOut.append(outputData)
            return True
        except ValueError:
            print('Import Error, .csv might be corrupted.')
            return False
