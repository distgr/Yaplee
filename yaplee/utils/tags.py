import random
from bs4 import BeautifulSoup

class TagManager:
    def __init__(self, loc) -> None:
        self.__tag_loc = loc
        self.__tags = {}
    
    def add(self, tag_name, **kwargs):
        tag_str = ', '.join(
            ['{}={}'.format(i, ('\''+str(str(j).replace('\'', '\\\''))+'\'')) for i, j in kwargs.items()]
        )
        unique_tag = str(tag_name)+'-_-'+str(random.randint(11111111, 99999999))
        self.__tags[unique_tag] = eval('BeautifulSoup("", "html.parser").new_tag({}, {})'.format(
            ('\''+(str(tag_name).replace('\'', '\\\''))+'\''),
            tag_str
        ))

    def __call__(self):
        return self.__tag_loc, self.__tags