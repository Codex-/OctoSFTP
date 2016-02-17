
# Python Modules
import glob, multiprocessing, os, shutil, subprocess

# Support Modules
from .config import AppConfig
from .client import ClientList
from .file import ClientFiles
from .server import ServerTasks


class OctoSFTP:
    """Main class for program"""

    def __init__(self, config_file='config.ini', client_file='clients.ini'):
        self.settings = AppConfig(config_file)
        self.clients = ClientList(self.settings, client_file)
        self.files = ClientFiles(self.settings, self.clients)

    def run(self):
        print(self.clients)
        self.files.run()
