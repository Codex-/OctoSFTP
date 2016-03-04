
# Python Modules
import glob, multiprocessing, os, shutil, subprocess

# Support Modules
from .config import AppConfig
from .client import ClientList
from .file import ClientFiles
from .server import ServerTasks
from .logging import Logger


class OctoSFTP:
    """Main class for program"""

    def __init__(self, config_file='config.ini', client_file='clients.ini'):
        self.settings = AppConfig(config_file)
        self.logging = Logger(self.settings)
        self.clients = ClientList(self.settings, client_file)
        self.files = ClientFiles(self.settings, self.clients)
        self.connection = ServerTasks(self.settings)

    def run(self):
        self.files.run()
        self.connection.run()