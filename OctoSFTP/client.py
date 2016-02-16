
import subprocess
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

        # Threading lock
        self.lock = Lock()

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
            #print("Online: " + client)
            self.clients_online.append(client)
            #return client, True
        else:
            #print("Offline: " + client)
            self.clients_offline.append(client)
            #return client, False

    def thread_dequeue(self):
        """
        Threadsafe queue support function to prevent conflicts
        :param thread: thread to receive data
        """
        while len(self.client_list) > 0:
            self.lock.acquire()
            client = self.client_list.pop()
            self.lock.release()

            # Pass popped client to function
            self.online_client_test(client)

    def online_clients(self):
        """
        Tests if all clients in client_list are online
        """
        active_threads = []

        # Spawn instances for multithreading
        for i in range(self.settings.client_threads):
            instance = Thread(target=self.thread_dequeue)
            active_threads.append(instance)
            instance.start()

        # Allow threads to complete before proceeding
        for instance in active_threads:
            instance.join()

        self.clients_online.sort()
        self.clients_offline.sort()

        # TODO: Add logging for successful list creation
        # TODO: create logging for offline cases