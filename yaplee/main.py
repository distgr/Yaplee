import sys, os, pathlib
from yaplee.app import app
from yaplee.sync import YapleeSync
from yaplee.meta import syncable

class YapleeManager:
    def __init__(self):
        self.user_path = os.getcwd()
        self.module_path = str(pathlib.Path(__file__).resolve().parent)
        self.argv = [argv.lower() for argv in sys.argv][1:]
        self.syncable = syncable
        self.sync_comment = '# Automaticlly added by yaplee'

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
            sync_with_app = ''

            if '--sync' in self.argv:
                sync_index = self.argv.index('--sync')
                if len(self.argv) <= sync_index+1:
                    sys.exit(print('[YapleeError]: You must enter web-framework name that you want to sync in `--sync`'))
                sync_with_app = self.argv[sync_index+1]
                if sync_with_app not in self.syncable:
                    sys.exit(print('[YapleeError]: Cannot sync yaplee new project with `{}`'.format(sync_with_app)))
                del self.argv[self.argv.index('--sync')]
                del self.argv[self.argv.index(sync_with_app)]

            app_name = eval('self.argv[1]') if len(self.argv) > 1 else 'yaplee_app.py'
            app_name = self.__format_app_name(app_name)

            print('Starting a yaplee blank application...')

            if sync_with_app:
                if sync_with_app == 'django':
                    if not os.path.isfile(os.path.join(self.user_path, 'manage.py')):
                        sys.exit(print('[YapleeError]: This is not a correct django path!'))
                    print('Syncing new project with your django project...')
                    with open(os.path.join(self.user_path, 'manage.py'), 'r+') as manage_py:
                        manage_py_data = manage_py.read().splitlines()
                        manage_py.close()
                        del manage_py
                    manage_py_data.insert(
                        manage_py_data.index('import sys')+1, 'from {} import myapp as yaplee_app {}'.format(
                            '.'.join(app_name.split('.')[:-1]),
                            self.sync_comment
                        )
                    )
                    django_exec_command = 'execute_from_command_line(sys.argv)'
                    django_execcommand_index = [i.strip() for i in manage_py_data].index(django_exec_command)
                    django_exec_command_tabs = manage_py_data[django_execcommand_index].split(django_exec_command)[0]
                    manage_py_data.insert(
                        django_execcommand_index,
                        '{}if yaplee_app.is_debug and \'runserver\' in sys.argv: {}\n{}yaplee_app.auto_sync(\'django\') {}'.format(
                            str(django_exec_command_tabs),
                            self.sync_comment,
                            str(django_exec_command_tabs)*2,
                            self.sync_comment
                        )
                    )
                    manage_py_data = '\n'.join(manage_py_data)
                    with open(os.path.join(self.user_path, 'manage.py'), 'w+') as manage_py:
                        manage_py.write(manage_py_data)
                        manage_py.close()
                        del manage_py
                    settings_file = ''
                    for r, d, f in os.walk(self.user_path):
                        for i in f:
                            if i == 'settings.py':
                                settings_file = os.path.join(r, i)
                                break
                    print((' '*3)+'- Project successfully synced with your django project.')

            with open(os.path.join(self.user_path, app_name), 'w+') as f:
                with open(os.path.join(self.module_path, 'assets', 'yaplee_app.py'), 'r+') as blankapp:
                    blankapp_data = blankapp.read()
                    if sync_with_app:
                        blankapp_data = blankapp_data.replace('\n# Start yaplee project (if you want to debug).', '')
                        blankapp_data = blankapp_data.replace('\nmyapp.start()', '')
                        blankapp_data = blankapp_data.replace('(debug=True)', '(debug=True, sync=\'django\')')
                    f.write(blankapp_data)
                    blankapp.close()
                    del blankapp
                f.close()
                del f
            print('Yaplee blank project created successfully!')
        else:
            print('[YapleeError]: No such command \'{}\''.format(' '.join(sys.argv[1:])))
        
        sys.exit()