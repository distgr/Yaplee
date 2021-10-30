import os
import sys
from yaplee.server import Server
from yaplee.meta import syncable
from yaplee.errors import (SetError, SyncError, InitialNotFound,
                            TemplateNotFound, PortOnUse, TemplateExist, UnknownTemplateValue)

class app:
    def __init__(self):
        if(os.geteuid() and os.name == 'posix'):
            sys.exit(
                print('Warning: Please run app in sudo')
            )
        self.__metabase = {
            'actions': {},
            'config': {'debug': True, 'sync': None, 'port': 8989, 'opentab': False},
            'tree': {},
            'templates': {}
        }
        self.__on_init = False
        self.user_path = os.getcwd()
        self.is_debug = self.__metabase['config']['debug']

    def init(self, initial_func):
        self.__metabase['actions']['initial'], self.__on_init = initial_func, True
        initial_func()
        self.__on_init = False

    def start(self):
        server = Server(self.__metabase)
        if not 'initial' in self.__metabase['actions']:
            raise InitialNotFound('Initial function is required for any yaplee project')
        if not self.__metabase['config']['debug']:
            return
        if self.__metabase['config']['sync']:
            return
        print('Starting yaplee debug development server...')
        print(((' '*3)+'- ')+'Tip: You can use `CTRL + C` to close development server')
        port = self.__metabase['config']['port']
        if not server.is_port_open():
            raise PortOnUse('{} port is on use, make sure another yaplee server is not started or {}'.format(str(port),
                ('use another port on your yaplee app config') if port != 8989 else
                ('change the yaplee development server port by adding \'port=...\' on yaplee server config')
            ))
        try:
            server.start()
        except KeyboardInterrupt:
            server.remove_yaplee_dir()

    def auto_sync(self, fw):
        if fw.lower() not in syncable:
            raise SyncError('Yaplee cannot sync with \'{}\''.format(fw))
        if os.environ.get('RUN_MAIN') != 'true':
            print('[Yaplee] : Preparing your application...')
            server = Server(self.__metabase)
            settings_py_path = os.path.join(self.user_path, self.user_path.split(os.path.sep)[-1], 'settings.py')
            with open(settings_py_path, 'r+') as settings_py_data:
                settings_py_data = settings_py_data.read()
            with open(settings_py_path, 'w+') as settings_py:
                if 'import os' not in settings_py_data:
                    settings_py_data = settings_py_data.replace('from pathlib import Path', "import os\nfrom pathlib import Path")
                if 'yaplee_dir' not in settings_py_data:
                    settings_py_data = settings_py_data.replace("'DIRS': [],", "'DIRS': [os.environ.get('yaplee_dir')],")
                settings_py.write(settings_py_data)
            os.environ['yaplee_dir'] = server.temp_path

    def template(self, template_path, **kwargs):
        if not os.path.isfile(template_path):
            raise TemplateNotFound('Template \'{}\' does not exist in your path'.format(template_path))
        def wrapper(func):
            template_meta = func()
            if type(template_meta) is not dict:
                raise UnknownTemplateValue(
                    'Your template `{}` returns a non-dict value'.format(template_path)
                )
            name = None if 'name' not in kwargs else kwargs['name']
            if template_path+'-_-' in self.__metabase['templates']:
                raise TemplateExist(
                    'You have already added a template ('+template_path+'), '
                    'you can add a special name to your template by adding `name=\'...\'` to template decorator'
                )
            elif template_path+'-_-'+str(name) in self.__metabase['templates']:
                raise TemplateExist(
                    'You have already added a template with '+template_path+' and ('+str(name)+') special name, '
                    'please change your template special name'
                )
            self.__metabase['templates'][template_path+'-_-'+('' if not name else name)] = {
                'func': func,
                'name': name,
                'load_name': None if 'load_name' not in kwargs else kwargs['load_name'],
                'meta': template_meta
            }
        return wrapper

    def add(self, **kwargs):
        if not self.__on_init:
            raise SetError('You can only use \'.add(...)\' in yaplee app initial function')
        print(kwargs)

    def tree(self, tree):
        self.__metabase['tree'] = tree

    def config(self, **kwargs):
        set_meta = self.__metabase['config']
        lower_kwargs = {kwarg.lower():val for kwarg, val in kwargs.items()}

        if not self.__on_init:
            raise SetError('You can only use \'.config(...)\' in yaplee app initial function')

        if 'debug' in lower_kwargs:
            set_meta['debug'] = lower_kwargs['debug']
            self.is_debug = set_meta['debug']

        if 'opentab' in lower_kwargs:
            set_meta['opentab'] = kwargs['opentab']

        if 'sync' in lower_kwargs:
            if lower_kwargs['sync'] not in syncable:
                raise SyncError('Yaplee cannot sync with \'{}\''.format(kwargs['sync']))
            set_meta['sync'] = lower_kwargs['sync']

        if 'port' in lower_kwargs:
            set_meta['port'] = lower_kwargs['port']

        self.__metabase['config'] = set_meta
