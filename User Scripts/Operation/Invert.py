from UserScript import UserOperation

class ds_user_script(UserOperation):
    name = 'Invert'
    tooltip = 'Invert Sign of Dataset Elements'

    def operation(self):
        print(self.name)