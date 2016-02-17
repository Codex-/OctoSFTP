
# Python Modules
import configparser, os
from multiprocessing import cpu_count

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
        self.server_temp_extension = ""
        self.server_conflict = ""

        # Local paths for files
        self.local_queue = ""
        self.local_processed = ""
        self.log_level = ""
        self.log_file = ""

        # File properties
        self.file_types = []
        self.file_minsize = 0
        self.file_attempts = 0

        # Client settings
        self.client_attempts = 0
        self.client_path = ""
        self.client_threads = 0
        self.client_connections = 0

        #

        try:
            if not os.path.exists(config_file):
                raise FileNotFoundError
        except FileNotFoundError:
            print("{0} not found.".format(config_file))
            exit()

        try:
            self.load_settings(config_file)
        except configparser.NoSectionError as missing:
            print("Failed to load settings.")
            print("{0}".format(missing))
            exit()

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
        self.server_port = self.config.getint("server", "port")
        self.server_dir = self.config.get("server", "dir")
        self.server_connections = self.config.getint("server", "connections")
        self.server_temp_extension = self.config.get("server", "temp_extension")
        self.server_conflict = self.config.get("server", "conflict")

        # Local paths for files
        self.local_queue = self.config.get("local", "queue")
        self.local_processed = self.config.get("local", "processed")

        # Set logging
        self.log_level = self.config.get("local", "log_level")
        self.log_file = self.config.get("local", "log_file")

        # File properties
        self.file_types = ["." + type.strip() for type in
                           (self.config.get("file", "type")).split(",")]
        self.file_minsize = self.config.getint("file", "minsize") * 1000
        self.file_attempts = self.config.getint("file", "attempts")

        # Client settings
        self.client_attempts = self.config.get("client", "attempts")
        self.client_path = (self.config.get("client", "path")).replace(":", "$")
        self.client_threads = self.config.getint("client", "threads")
        self.client_connections = self.config.getint("client", "connections")

        # Validate local paths exist
        self.validate_path(self.local_queue)
        self.validate_path(self.local_processed)

        # Validate values for threading aren't too high
        self.server_connections = self.validate_threads(self.server_connections)
        self.client_threads = self.validate_threads(self.client_threads)


    def validate_path(self, path):
        """
        Check path specified exists, create if not.

        :param path: Path to be checked
        """
        # TODO: move path validation into function on init.
        # TODO: If path is valid, os.chrdir to correct path
        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except PermissionError as error:
            print(error)
            print("Permission denied: Is the drive selected valid?")
            print("Update your configuration and try again.")
            exit()

    def validate_threads(self, thread_value):
        """
        Checks if the value used for thread count is compatible with system.

        :param thread_value:
        :return:
        """
        return min(cpu_count(), (max(1, thread_value)))