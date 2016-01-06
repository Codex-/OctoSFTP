
# Python Modules
import glob, pysftp, multiprocessing, os, shutil, subprocess
from .config import AppConfig

# Support Modules
# TODO: Split this program out later.


class OctoSFTP:
    """Main class for program"""

    def __init__(self, config_file='config.ini', client_file='clients.ini'):

        self.settings = AppConfig(config_file)
        self.clients = ClientList(self.settings, client_file)


    def run(self):
        print(self.clients)



class ClientList:
    """Stores client list and support functions for testing clients online"""

    def __init__(self, settings, client_file):
        """Initialises the class"""
        self.client_list = []

        self.clients_online = []
        self.clients_offline = []

        self.settings = settings
        self.client_file = client_file

        # Begins populating class lists
        self.load_client_file()
        self.online_clients()

    def __str__(self):
        """Returns count of offline and online clients"""
        return "{0} online clients. {1} offline clients.".format(
            len(self.clients_online), len(self.clients_offline))

    def load_client_file(self):
        """
        Loads the clients from file
        """
        client_file = open(self.client_file, "r")

        with client_file:
            self.client_list = [client.strip() for client in client_file
                                if client.find("#") < 0 and client != "\n"]

    def online_client_test(self, client):
        """
        Pings the client to test if online

        :param client: Client to test if online
        :return: Tuple of client name and online status: (client, Bool)
        """
        online = subprocess.call("ping -n " +
                                 self.settings.client_attempts +
                                 " " +
                                 client,
                                 stdout=subprocess.PIPE
                                 )

        if online == 0:
            return client, True
        else:
            return client, False

    def online_clients(self):
        """
        Tests if all clients in client_list are online
        """
        # Spawn a pool for multithreading
        process_pool = multiprocessing.Pool(
            processes=self.settings.client_threads
        )

        # Populate pool and begin
        pool_results = process_pool.map(self.online_client_test,
                                        self.client_list)

        for client in pool_results:
            if client[1]:
                self.clients_online.append(client[0])
            else:
                self.clients_offline.append(client[0])

        print(self.clients_online)
        self.clients_online.sort()
        self.clients_offline.sort()

        # TODO: Add logging for successful list creation
        # TODO: create logging for offline cases


class ClientFiles:
    """Processes the clients files to be moved etc"""

    def __init__(self, settings, clients):
        self.settings = settings
        self.clients = clients

        # Dictionary of files to be moved, client is key
        self.client_files = dict()

        # Path templates
        self.file_path = ("\\\\{0}\\" +
                          self.settings.client_path +
                          "\\" +
                          "*" +
                          self.settings.file_type)

        self.build_file_list()

    def file_list(self, client):
        """
        Creates a list of files for each client to be moved

        :param client: Client to have file list generated
        :return: Client files if any, otherwise returns None
        """
        client_files = (glob.glob(self.file_path.format(client)))

        if len(client_files) > 0:
            client_files = [file for file in client_files
                            if os.stat(file).st_size >=
                            self.settings.file_minsize]

            if len(client_files) > 0:
                return client, client_files

        return  # TODO: Check if needed

    def build_file_list(self):
        """
        Processes clients to construct class file list
        """
        # Spawn a pool for multithreading
        process_pool = multiprocessing.Pool(
            processes=self.settings.client_connections
        )

        # Populate pool and begin
        pool_results = process_pool.map(self.file_list,
                                        self.clients.clients_online)

        for client_results in pool_results:
            if client_results:
                self.client_files[client_results[0]] = client_results[1]

        print(self.client_files)

    def move_files(self, file_list):
        """
        Move files from client to local store. This is done as a list per client
        so as to not flood a specific sites WAN link and cause issues with
        stores connectivity.

        :param file_list:
        :return:
        """
        for file in file_list:
            if os.path.isfile(file):
                pass

        pass


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
