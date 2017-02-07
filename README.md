OctoSFTP
=========

A program written in Python 3 to move files from network clients to an SFTP
server.

What's the point?
-----------------
This program was created in response to requiring to pull 7z/zip diagnostic
files from various client PC's and upload them to the supplier/vendor diagnostic
SFTP server via automation.


Features of OctoSFTP
---------------------

 - Multiple connections to SFTP server.
 - Multiple client connections.
 - Configurable file extension to search for.


How to install
--------------
Simply git clone the repository locally, and use the example configuration file
as a base for configuring for your own environment.

#### Install dependencies

To install dependencies, run

    pip install -r requirements.txt
    

Using Octo-SFTP
---------------

#### Configure config.ini

An example configuration is supplied.
Most of the example config is self-explanatory.

The number of SFTP server connections to establish:
    
    [server]
    connections = 2
    
The number of clients to connect to at a time for pulling files:

    [client]
    connections = 4
    
Both of these should be set according to the bandwidth available over the
network, too high and you may cause issues for other users (worst case.)

#### Configure clients.ini

Add clients requiring files to be moved into the `clients.ini` file:

    # Example Category
    clientpc01
    clientpc02
    
    # Example Category 2
    clientpc03
    clientpc04


Development
------------

#### virtualenv

It is recommended to run and develop this program in a virtualenv.

To create a new virtualenv, first install virtualenv:

    pip install virtualenv
    
Create a virtualenv instance, replacing `octosftp` with your choice of name

    virtualenv octosftp
    
The directory this is installed in is relative to the shell path you will have
currently selected. The below will run your virtualenv
Windows:

    ".\octosftp\Scripts\activate"
    
Linux:

    source ./octosftp/bin/activate
    

License
-------

Octo-SFTP is licensed under the [MIT License](LICENSE).