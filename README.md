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
    
#### Using Octo-SFTP

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