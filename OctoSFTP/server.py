
# python modules
import os, pysftp
from threading import Thread, Lock

# TODO: Rewrite to support multiple connections to server

class ServerTasks:

    def __init__(self, config, files=None):
        self.config = config

        # Establish class connection
        self.connection = self.connect() # TODO: See if multipool working with connections this way

        self.files = files

    def connect(self):
        """
        Establish connection with the SFTP server.
        :return: Object with established connection to SFTP server.
        """
        # TODO: Create try and except so this actually doesn't blow up
        # TODO: The exception is pysftp.Connection.Exception
        # TODO: paramiko.ssh_exception.AuthenticationException
        # TODO: paramiko.ssh_exception.SSHException <- port wrong
        return pysftp.Connection(self.config.server_address,
                                 username=self.config.server_username,
                                 password=self.config.server_password,
                                 port=self.config.server_port)

    def disconnect(self):
        """
        Close connection to server safely
        """
        self.connection.close()

    def set_path(self, path):
        """

        :param path:
        """
        self.connection.chdir(path)

    def file_exists(self, file):
        """
        If config is set to:
         - Replace file: Simply remove the file from server.
         - Rename file : Recursively calls itself until an available file name
                         is available.

        :param file:
        """
        if self.connection.exists(file):
            if self.config.server_conflict == "replace":
                self.connection.remove(file)
            elif self.config.server_conflict == "rename":
                # TODO: Change this to work with numbering because _old
                # is unintuitive
                old_file = file.replace(self.config.file_type,
                                        "_old" +
                                        self.config.file_type)
                if self.connection.exists(old_file):
                    self.file_exists(old_file)
                else:
                    self.connection.rename(file, (file.replace
                                                  (self.config.file_type,
                                                   "_old" +
                                                   self.config.file_type)))

    def upload_file(self, file):
        """

        :param file:
        :return:
        """

        # Change to specified queue folder
        # TODO: Probably move to parent function and not in support function
        os.chdir(self.config.local_queue)

        uploaded_file = os.rename(file, (file.replace
                                         (self.config.file_type,
                                          self.config.server_temp_extension)))

        self.file_exists(file)

        # Begin upload
        try:
            self.connection.put(uploaded_file, preserve_mtime=True)
            self.connection.rename(uploaded_file, file)
            return True
        except:
            return False

    def run(self):
        """
        Execute server tasks
        """
        if self.files:
            for file in self.files:
                self.upload_file(file)
