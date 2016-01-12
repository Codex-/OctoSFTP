
import glob, multiprocessing, os

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


