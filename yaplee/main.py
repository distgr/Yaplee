import sys, os, pathlib
from yaplee.sync import YapleeSync

class YapleeManager:
    def __init__(self):
        self.user_path = os.getcwd()
        self.module_path = str(pathlib.Path(__file__).resolve().parent)
        self.argv = [argv.lower() for argv in sys.argv]
        self.argv.pop(0)

        print('Usage: Yaplee {commands...}')