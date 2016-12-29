from UserScript import UserOperation

class ds_user_script(UserOperation):
    name = 'Clone - Invert'
    tooltip = 'Clone Dataset to Produce Two Identical (But Inverted) Datasets'

    def operation(self):
        print(self.name)