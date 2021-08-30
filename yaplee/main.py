import sys, os, pathlib
from yaplee.app import app
from yaplee.sync import YapleeSync

class YapleeManager:
    def __init__(self):
        self.user_path = os.getcwd()
        self.module_path = str(pathlib.Path(__file__).resolve().parent)
        self.argv = [argv.lower() for argv in sys.argv][1:]

        self.__check_argv()

    def __format_app_name(self, app_name, number_slot=1, sep='-'):
        app_name = app_name+'.py' if not app_name.endswith('.py') else app_name
        if os.path.isfile(os.path.join(self.user_path, app_name)):
            if sep in app_name:
                app_name = sep.join(app_name.split(sep)[1:])
            return self.__format_app_name(
                '{}{}{}'.format(str(number_slot), sep, app_name),
                number_slot=number_slot+1
            )
        return app_name

    def __print_subs(self, part_name, options, tabs=3, exit=False):
        if part_name:
            print(part_name.title()+':')
        for op, description in options.items():
            if type(op) is dict:
                self.__print_subs(op, description, tabs=tabs*2)
                continue
            print((' '*tabs)+'- '+op+('\n'+(' '*tabs)+' '*6)+description.capitalize())
        if exit:
            sys.exit()
    
    def __check_argv(self):
        if not self.argv:
            print('\nUsage: yaplee [OPTIONS] COMMAND [ARGS]...\n')
            self.__print_subs('commands', {
                'new [name]': 'to create a yaplee blank file',
            }, exit=True)
        
        if self.argv[0] == 'new':
            app_name = eval('self.argv[1]') if len(self.argv) > 1 else 'yaplee_app.py'
            app_name = self.__format_app_name(app_name)
            with open(os.path.join(self.user_path, app_name), 'w+') as f:
                with open(os.path.join(self.module_path, 'assets', 'yaplee_app.py'), 'r+') as blankapp:
                    blankapp_data = blankapp.read()
                    f.write(blankapp_data)
                    blankapp.close()
                    del blankapp
                f.close()
                del f
            print('Yaplee blank project created successfully.')
        else:
            print('[YapleeError]: No such command \'{}\''.format(' '.join(sys.argv[1:])))
        
        sys.exit()