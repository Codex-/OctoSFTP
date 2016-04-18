
# Python Modules
import glob, multiprocessing, os, shutil, subprocess

# Support Modules
from .config import AppConfig
from .client import ClientList
from .file import ClientFiles
from .server import ServerTasks
from .logging import load_logging

import logging


class OctoSFTP:
    """Main class for program"""

    def __init__(self, config_file='config.ini', client_file='clients.ini'):
        self.settings = AppConfig(config_file)
        self.logging = load_logging(self.settings.log_file,
                                    self.settings.log_level)
        self.clients = ClientList(self.settings, client_file)
        self.files = ClientFiles(self.settings, self.clients)
        self.connection = ServerTasks(self.settings)

    def run(self):
        self.files.run()
        self.connection.run()