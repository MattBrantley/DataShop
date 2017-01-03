from UserScript import *

class ds_user_script(UserImport):
    name = 'CSV Importer Type1'
    registeredFiletypes = {'Column Separated CSV': '.csv', 'Something Else': '.SomethingElse'}

    def import_func(self, URL):
        try:
            data = np.genfromtxt(URL, delimiter=',')
        except ValueError:
            print('Import Error, .csv might be corrupted.')

        return data