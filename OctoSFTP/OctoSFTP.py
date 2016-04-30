
import logging

from .config import AppConfig
from .client import ClientList
from .file import ClientFiles
from .server import ServerTasks
from .logging import load_logging


class OctoSFTP:
    """Main class for program"""

    def __init__(self, config_file='config.ini', client_file='clients.ini'):
        self.settings = AppConfig(config_file)
        self.logging = load_logging(self.settings.log_file,
                                    self.settings.log_level)

        # Local logger
        self._logger = logging.getLogger(__name__)

        self.clients = ClientList(self.settings, client_file)
        self.files = ClientFiles(self.settings, self.clients)
        self.connection = ServerTasks(self.settings)

    def run(self):
        try:
            self.files.run()
            self.connection.run()
        except Exception as error:
            self._logger.log(logging.CRITICAL, str(error))
