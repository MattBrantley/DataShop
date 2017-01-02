from UserScript import *

class ds_user_script(UserOperation):
    name = 'CSV Importer v0.1'

    def import_func(self, URLs):
        if fname[0]:
            try:
                data = np.genfromtxt(fname[0], delimiter=',')
                name = self.cleanStringName(os.path.basename(fname[0]))
                data = {'GUID': self.saveDSToSql(name, data), 'Type': 'Data', 'Name': name}
                self.addItem(self.root, data)
                self.saveWSToSql()
            except ValueError:
                print('Import Error, .csv might be corrupted.')