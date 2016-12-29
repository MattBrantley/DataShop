from UserScript import UserOperation

class ds_user_script(UserOperation):
    name = 'Multiply'
    tooltip = 'Multiply the data set by itself'

    def operation(self):
        print(self.name)