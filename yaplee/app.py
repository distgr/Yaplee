import os
from yaplee.server import Server
from yaplee.errors import (SetError, SyncError, InitialNotFound,
                            TemplateNotFound, PortOnUse, TemplateExist, UnknownTemplateValue)

class app:
    def __init__(self):
        self.__metabase = {
            'actions': {},
            'config': {'debug': True, 'sync': None, 'port': 8989, 'opentab': False},
            'tree': {},
            'templates': {}
        }
        self.__on_init = False
        self.is_debug = self.__metabase['config']['debug']

    def init(self, initial_func):
        self.__metabase['actions']['initial'], self.__on_init = initial_func, True
        initial_func()
        self.__on_init = False
    
    def start(self):
        server = Server(self.__metabase)
        if not 'initial' in self.__metabase['actions']:
            raise InitialNotFound('Initial function is required for any yaplee project')
        print('Loading your yaplee project meta...')
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
        allowed_sync_types = ('django',)
        lower_kwargs = {kwarg.lower():val for kwarg, val in kwargs.items()}

        if not self.__on_init:
            raise SetError('You can only use \'.config(...)\' in yaplee app initial function')
        
        if 'debug' in lower_kwargs:
            set_meta['debug'] = lower_kwargs['debug']
            self.is_debug = set_meta['debug']
        
        if 'opentab' in lower_kwargs:
            set_meta['opentab'] = kwargs['opentab']

        if 'sync' in lower_kwargs:
            if lower_kwargs['sync'] not in allowed_sync_types:
                raise SyncError('Yaplee cannot sync with \'{}\''.format(kwargs['sync']))
            set_meta['sync'] = lower_kwargs['sync']
        
        if 'port' in lower_kwargs:
            set_meta['port'] = lower_kwargs['port']
        
        self.__metabase['config'] = set_meta