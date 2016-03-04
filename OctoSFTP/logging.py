
import logging, os

#TODO logging everything

class Logger:

    def __init__(self, settings):
        self.settings = settings

        # Initialise logging and log file
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level())

        self.handler = logging.FileHandler(self.settings.log_file)
        self.handler.setLevel(self.level())

        # Set logging format string
        self.template = logging.Formatter("%(asctime)s - "
                                        "%(name)s - "
                                        "%(levelname)s - "
                                        "%(message)s")

        # Assign format string to handler
        self.handler.setFormatter(self.template)

        self.logger.addHandler(self.handler)

        print("try log this thing")
        self.logger.info("Test")

    def level(self):
        """
        Determines logging level to set on handler

        :return: logging level
        """
        if (self.settings.log_level).upper() == "CRITICAL":
            return logging.CRITICAL
        elif (self.settings.log_level).upper() == "ERROR":
            return logging.ERROR
        elif (self.settings.log_level).upper() == "DEBUG":
            return logging.DEBUG
        else:
            return logging.INFO