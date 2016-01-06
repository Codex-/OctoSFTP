
# python modules
import pysftp

class ServerTasks:

    def __init__(self, settings):
        self.settings = settings

    def connect(self):
        """
        Establish connection with the SFTP server.
        :return: Object with established connection to SFTP server.
        """
        # TODO: Create try and except so this actually doesn't blow up
        return pysftp.Connection(self.settings.server_address,
                                 username=self.settings.server_username,
                                 password=self.settings.server_password,
                                 port=self.settings.server_port)
