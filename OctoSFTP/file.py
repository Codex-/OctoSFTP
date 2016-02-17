
import glob, multiprocessing, os, time, shutil
from threading import Thread, Lock


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
                          "*")# +
                          #self.settings.file_type)

        # Threading lock
        self.lock = Lock()

        #self.build_file_list()

    def file_list(self, client):
        """
        Creates a list of files for each client to be moved

        :param client: Client to have file list generated
        :return: Client files if any, otherwise returns None
        """
        #client_files = (glob.glob(self.file_path.format(client)))

        # client_files = [glob.glob(self.file_path + file_type)
        #                 for file_type in self.settings.file_types]

        client_files = []

        for file_type in self.settings.file_types:
            client_files.extend(glob.glob(self.file_path.format(client) +
                                          file_type))

        if len(client_files) > 0:
            client_files = [file for file in client_files
                            if os.stat(file).st_size >=
                            self.settings.file_minsize]

            if len(client_files) > 0:
                #print(client, client_files)
                self.client_files[client] = client_files
                #return client, client_files

        #return  # TODO: Check if needed

    def thread_file_list(self):
        """
        Threadsafe queue support function to prevent conflicts
        :param thread: thread to receive data
        """
        client_list = self.clients.clients_online

        while len(client_list) > 0:
            self.lock.acquire()
            client = client_list.pop()
            self.lock.release()

            # Pass popped client to function
            self.file_list(client)

    def build_file_list(self):
        """
        Processes clients to construct class file list
        """
        active_threads = []

        # Spawn instances for multithreading
        for i in range(self.settings.client_connections):
            instance = Thread(target=self.thread_file_list)
            active_threads.append(instance)
            instance.start()

        # Allow threads to complete before proceeding
        for instance in active_threads:
            instance.join()

    def thread_move_files(self):

        while len(self.client_list) > 0:
            self.lock.acquire()
            client = self.client_list.pop()
            self.lock.release()

            # Pass popped client to function
            self.move_files(self.client_files[client])

    def move_files(self, file_list):
        print(file_list)
        for file in file_list:
            print(os.path.basename(file))
            os.chdir(self.settings.local_queue)

            # Check if file exists locally already
            if os.path.exists(os.path.basename(file)):
                os.remove(os.path.basename(file))
                #todo log that it had to delete it

            try:
                shutil.move(file, self.settings.local_queue)
            except OSError as error:
                # Todo log that error g
                print(error)




    def build_move_files(self):
        """
        Move files from client to local store. This is done as a list per client
        so as to not flood a specific sites WAN link and cause issues with
        stores connectivity.

        :param file_list:
        """
        active_threads = []
        self.client_list = list(self.client_files.keys())

        for i in range(self.settings.client_connections):
            instance = Thread(target=self.thread_move_files)
            active_threads.append(instance)
            instance.start()

        # Allow threads to complete before proceeding
        for instance in active_threads:
            instance.join()


    def run(self):
        self.build_file_list()
        # for i in range(len(self.clients)):
        #     self.clients.pop()
        #print(self.client_files)

        #self.build_move_files()



