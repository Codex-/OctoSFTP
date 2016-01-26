
import subprocess
from multiprocessing import cpu_count
from threading import Lock, Thread

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