import os
import random
import tempfile
import webbrowser
import time
import uuid
import socket
import shutil
import subprocess
import pathlib
from bs4 import BeautifulSoup
from yaplee.errors import UnknownTemplateValue

class Server:
    def __init__(self, meta) -> None:
        self.port = meta['config']['port']
        self.templates = meta['templates']
        self.tree = meta['tree']
        self.opentab = meta['config']['opentab']
        self.tempuuid = ''
        self.module_path = str(pathlib.Path(__file__).resolve().parent)
    
    def is_port_open(self):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_connection = ('127.0.0.1', self.port)
        port_open = a_socket.connect_ex(local_connection)
        a_socket.close()
        return not (not port_open)

    def __gen_yaplee_temp(self):
        self.tempuuid = uuid.uuid1().hex[:15]
        path = os.path.join(tempfile.gettempdir(), self.tempuuid)
        if not os.path.isdir(path):
            os.mkdir(path)
        return self.tempuuid, path
    
    def start(self):
        generated_files = []
        js_functions = {}
        temp_uuid, temp_path = self.__gen_yaplee_temp()
        
        for template, meta in self.templates.items():
            template = template.split('-_-')[0]
            to_copy_path = meta['load_name'] if meta['load_name'] else template
            template_to_copy = os.path.join(temp_path, to_copy_path.replace('\\', '/' if os.name == 'posix' else '\\'))
            shutil.copy(
                template,
                template_to_copy
            )

            tag_loc, tags = '', {}

            if 'tags' in meta['meta']:
                tag_loc, tags = meta['meta']['tags']()
                
                for tag_meta, tag in tags.items():
                    tag_source = ''
                    is_tag_has_source = False
                    tag_name = str(tag_meta.split('-_-')[0])
                    if tag_name in ['link']:
                        if 'href' in str(tag):
                            tag_source = tag.get('href')
                            is_tag_has_source = True
                    else:
                        try:
                            if 'src' in str(tag):
                                tag_source = tag.get('src')
                                is_tag_has_source = True
                        except:
                            continue
                    if is_tag_has_source and ('://' not in tag_source and tag_source):
                        shutil.copy(
                            tag_source,
                            os.path.join(temp_path, tag_source)
                        )
                    if 'tagvalue' in tag.attrs:
                        tagvalue = tag.get('tagvalue')
                        del tag.attrs['tagvalue']
                        tag.append(tagvalue)
            
            elif 'functions' in meta['meta']:
                js_functions = {i.__name__:i for i in meta['meta']['functions']}
                        
            elif 'style' in meta['meta']:
                if type(meta['meta']['style']) is str:
                    styles = [meta['meta']['style']]
                elif type(meta['meta']['style']) is list:
                    styles = meta['meta']['style']
                else:
                    raise UnknownTemplateValue(
                        'template style must be list or string (one style)'
                    )
                tag_loc, tags = 'head', {
                    str(random.randint(111111, 999999)):BeautifulSoup('', 'html.parser').new_tag(
                        'link', rel='stylesheet', href=style
                    ) for style in styles
                }
                for style in styles:
                    shutil.copy(
                        style,
                        os.path.join(temp_path, style)
                    )
                
            with open(template_to_copy, 'r+') as file:
                template_data = file.read()
                soup = BeautifulSoup(template_data, 'html.parser')
                for tagname, tag in tags.items():
                    soup.find(tag_loc).append(tag)
                for funcname, function in js_functions.items():
                    unique_id = str(uuid.uuid1()).split('-')[0]
                    soup.html.append(soup.new_tag('script', id=unique_id))
                    soup.find('script', {'id': unique_id}).append(
                        'function '+funcname+'(){ '+
                        '\n'.join([i for i in function()])+
                        ' }'
                    )
                file.truncate(0)
                file.write(soup.prettify())
                del file

            generated_files.append(to_copy_path)

        if 'index.html' not in generated_files:
            with open(os.path.join(self.module_path, 'assets', 'no-index.html.py'), 'r+') as file:
                nohtml_base = file.read()
                file.close()
                del file
            nohtml_base = nohtml_base.replace('{% avaliable_paths %}', 
                '' if not self.templates else
                '<h4>Avaliable paths : {}</h4>'.format(
                    ', '.join(['<a href="{}" target="_blank">{}</a>'.format(
                            i.split('-_-')[0] if j['load_name'] == None else j['load_name'],
                            i if not j['name'] else j['name'].title()
                    ) for i, j in self.templates.items()])
                )
            )
            with open(os.path.join(temp_path, 'index.html'), 'w+') as file:
                file.write(nohtml_base)

        if self.opentab:
            webbrowser.open('http://127.0.0.1:{}/'.format(str(self.port)))
            time.sleep(1)
        subprocess.run(
            ('python3' if os.name == 'posix' else 'python')+' -m http.server '+str(self.port)+' --bind 127.0.0.1 --directory "'+temp_path+'"',
            shell=True
        )
    
    def remove_yaplee_dir(self):
        if os.path.isdir(os.path.join(tempfile.gettempdir(), self.tempuuid)):
            shutil.rmtree(os.path.join(tempfile.gettempdir(), self.tempuuid))
    