
# python modules
import os, pysftp, glob, shutil
from threading import Thread, Lock

# TODO: Rewrite to support multiple connections to server

class ServerTasks:

    def __init__(self, config, files=None):
        self.settings = config

        # Threading lock
        self.lock = Lock()

        # Establish class connection
        #self.connection = self.connect()

        self.dir = []

    def file_list(self):
        for file_type in self.settings.file_types:
            self.dir.extend(glob.glob(self.settings.local_queue +
                                      "/*" +
                                      file_type))

        self.files = [os.path.basename(file) for file in self.dir]
        self.files.sort()

        print(self.files)

    def connect(self):
        """
        Establish connection with the SFTP server.
        :return: Object with established connection to SFTP server.
        """

        try:
            return pysftp.Connection(self.settings.server_address,
                                     username=self.settings.server_username,
                                     password=self.settings.server_password,
                                     port=self.settings.server_port)
        except pysftp.AuthenticationException as error:
            print("auth")
            print(error)
            exit()
        except pysftp.ConnectionException as error:
            print("connection")
            print(error)
            exit()
        except pysftp.SSHException as error:
            # Todo: Log these
            print("port or address")
            print(error)
            exit()

    def file_exists(self, connection, file):
        """
        If config is set to:
         - Replace file: Simply remove the file from server.
         - Rename file : Recursively calls itself until an available file name
                         is available.

        :param file:
        """
        if connection.exists(file):
            if self.settings.server_conflict == "replace":
                connection.remove(file)
            elif self.settings.server_conflict == "rename":
                # TODO: Change this to work with numbering because _old
                # is unintuitive
                old_file = file.replace(self.settings.file_type,
                                        "_old" +
                                        self.settings.file_type)
                if connection.exists(old_file):
                    self.file_exists(connection, old_file)
                else:
                    connection.rename(file, (file.replace
                                             (self.settings.file_type,
                                                   "_old" +
                                                   self.settings.file_type)))

    def upload_file(self, connection, file):
        """

        :param file:
        :return:
        """
        # Change to specified queue folder
        os.chdir(self.settings.local_queue)

        # Rename files extension to specified temp extension
        os.rename(file, (file.replace
                         (os.path.splitext(file)[1],
                          self.settings.server_temp_extension)))

        upload_file = file.replace(os.path.splitext(file)[1],
                                   self.settings.server_temp_extension)

        # Check if either file exists on server
        self.file_exists(connection, file)
        self.file_exists(connection, file.replace
                         (os.path.splitext(file)[1],
                          self.settings.server_temp_extension))

        # Begin upload
        try:
            print("Uploading: " + file)
            connection.put((self.settings.local_queue +
                            "/" +
                            upload_file),
                           preserve_mtime=True)
            connection.rename(upload_file, file)

            # Return local file to original name
            os.rename(upload_file, file)

            # Move file to completion folder
            if os.path.isfile(self.settings.local_processed + "/" + file):
                dest_file = self.settings.local_processed + "/" + file
                orig_file = self.settings.local_queue + "/" + file
                if os.stat(dest_file).st_size == os.stat(orig_file).st_size:
                    # filename matches and size matches, file can removed.
                    os.remove(orig_file)
                elif os.stat(dest_file).st_size > os.stat(orig_file).st_size:
                    # File in processed folder is larger, remove new file
                    os.remove(orig_file)
                else:
                    os.remove(dest_file)
                    shutil.move(self.settings.local_queue + "/" + file,
                        self.settings.local_processed)
            else:
                shutil.move(self.settings.local_queue + "/" + file,
                            self.settings.local_processed)

        except IOError as error:
            print(error)
            print(file)
            os.rename(upload_file, file)
            raise IOError

    def thread_file_list(self):
        """
        Threadsafe queue support function to prevent conflicts
        """
        # Establish connection for this thread
        connection = self.connect()

        # Set working directory on server
        connection.chdir(self.settings.server_dir)

        while len(self.files) > 0:
            self.lock.acquire()
            file = self.files.pop()
            self.lock.release()

            # Pass popped file to function
            try:
                self.upload_file(connection, file)
            except EOFError as error:
                print(error)
                print("Connection lost during transfer")
                # Establish connection for this thread
                connection = self.connect()

                # Set working directory on server
                connection.chdir(self.settings.server_dir)

                # Lock and append filename to list to retry
                self.lock.acquire()
                self.files.append(file)
                self.lock.release()

            except FileNotFoundError as error:
                print(error)
                print("file missing yee yee")
                print("attempted to move", file)
                # Todo Log file as missing

            except IOError:
                self.lock.acquire()
                self.files.append(file)
                self.lock.release()

        connection.close()

    def build_file_list(self):

        active_threads = []

        for i in range(self.settings.server_connections):
            instance = Thread(target=self.thread_file_list)
            active_threads.append(instance)
            instance.start()

        for instance in active_threads:
            instance.join()


    def run(self):
        """
        Execute server tasks
        """
        # Todo: FileNotFoundError
        self.file_list()
        self.build_file_list()