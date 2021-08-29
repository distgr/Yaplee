import os, pathlib

class YapleeSync:
    def __init__(self, argv, _type='django') -> None:
        self.user_path = os.getcwd()
        self.module_path = str(pathlib.Path(__file__).resolve().parent)