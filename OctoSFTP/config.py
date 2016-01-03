
import configparser, os

class AppConfig:
    """Class for hosting the application settings as loaded from the supplied
        ini file"""

    def __init__(self, config_file):
        # Config Parser init
        self.config = configparser.ConfigParser()
        self.loaded = False

        # Server
        self.server_username = ""
        self.server_password = ""
        self.server_address = ""
        self.server_port = 0
        self.server_dir = ""
        self.server_connections = 0

        # Local paths for files
        self.local_queue = ""
        self.local_processed = ""

        # File properties
        self.file_type = ""
        self.file_minsize = 0
        self.file_attempts = 0

        # Client settings
        self.client_attempts = 0
        self.client_path = ""
        self.client_threads = 0
        self.client_connections = 0

        try:
            if not os.path.exists(config_file):
                raise FileNotFoundError
        except FileNotFoundError:
            print("{0} not found.".format(config_file))
            return

        try:
            self.load_settings(config_file)
        except configparser.NoSectionError as missing:
            print("Failed to load settings.")
            print("{0}".format(missing))

    def load_settings(self, file):
        """
        Loads application settings from text file

        :param file: file to be parsed for settings
        """
        self.config.read(file)

        # Server
        self.server_username = self.config.get("server", "username")
        self.server_password = self.config.get("server", "password")
        self.server_address = self.config.get("server", "address")
        self.server_port = int(self.config.get("server", "port"))
        self.server_dir = self.config.get("server", "dir")
        self.server_connections = int(self.config.get("server", "connections"))

        # Local paths for files
        try:
            if not os.path.exists(self.config.get("local", "queue")):
                raise FileNotFoundError
            else:
                self.local_queue = self.config.get("local", "queue")
        except FileNotFoundError:
            print("{0} does not exist.".format(
                self.config.get("local", "queue")))
            return

        try:
            if not os.path.exists(self.config.get("local", "processed")):
                raise FileNotFoundError
            else:
                self.local_processed = self.config.get("local", "processed")
        except FileNotFoundError:
            print("{0} does not exist.".format(
                self.config.get("local", "processed")))
            return

        # File properties
        self.file_type = "." + self.config.get("file", "type")
        self.file_minsize = int(self.config.get("file", "minsize")) * 1000
        self.file_attempts = int(self.config.get("file", "attempts"))

        # Client settings
        self.client_attempts = self.config.get("client", "attempts")
        self.client_path = (self.config.get("client", "path")).replace(":", "$")
        self.client_threads = int(self.config.get("client", "threads"))
        self.client_connections = int(self.config.get("client", "connections"))

        self.loaded = True