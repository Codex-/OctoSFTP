Octo-SFTP
=========

A program written in Python 3 to move files from network clients to an SFTP
server.

Features of Octo-SFTP
---------------------

 - Multiple connections to SFTP configurable
 - 

How to install
--------------
Good question, will flesh out proper instructions later.

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

    ./octosftp/Scripts/activate
    


License
-------

Octo-SFTP is licensed under the [MIT License](LICENSE).