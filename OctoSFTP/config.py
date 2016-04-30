
import configparser
import logging
import os


class AppConfig:
    """Class for hosting the application settings as loaded from the supplied
        ini file"""

    def __init__(self, config_file='config.ini'):
        # Config Parser init
        self.config = configparser.ConfigParser()

        try:
            if not os.path.exists(config_file):
                raise FileNotFoundError
            else:
                self.config.read(config_file)
        except FileNotFoundError:
            print("{0} not found.".format(config_file))
            exit()

        try:
            # Server
            self.server_username = self.config.get("server", "username")
            self.server_password = self.config.get("server", "password")
            self.server_address = self.config.get("server", "address")
            self.server_port = self.config.getint("server", "port")
            self.server_dir = self.config.get("server", "dir")
            self.server_connections = self.config.getint("server",
                                                         "connections")
            self.server_temp_extension = self.config.get("server",
                                                         "temp_extension")
            self.server_conflict = self.config.get("server", "conflict")

            # Local paths for files
            self.local_queue = self.config.get("local", "queue")
            self.local_processed = self.config.get("local", "processed")

            # Set logging
            self.log_level = self.log_level_check(self.config.get("local",
                                                                  "log_level"))
            self.log_file = self.config.get("local", "log_file")

            # File properties
            self.file_types = ["." + types.strip() for types in
                               (self.config.get("file", "type")).split(",")]
            self.file_minsize = self.config.getint("file", "minsize") * 1000
            self.file_attempts = self.config.getint("file", "attempts")

            # Client settings
            self.client_attempts = self.config.get("client", "attempts")
            self.client_path = (self.config.get("client", "path")).replace(":",
                                                                           "$")
            self.client_threads = self.config.getint("client", "threads")
            self.client_connections = self.config.getint("client",
                                                         "connections")

        except configparser.NoSectionError as missing:
            print("Failed to load settings.")
            print("{0}".format(missing))
            exit()

    @staticmethod
    def validate_path(path):
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

    @staticmethod
    def log_level_check(level):
        """
        Determines logging level to set on handler

        :return: logging level
        """
        level = level.upper()

        if level == "CRITICAL":
            return logging.CRITICAL
        elif level == "ERROR":
            return logging.ERROR
        elif level == "WARNING":
            return logging.WARNING
        elif level == "DEBUG":
            return logging.DEBUG
        else:
            return logging.INFO
