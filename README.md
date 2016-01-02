Octo-SFTP
=========

A program written in Python 3 to move files from network clients to an SFTP
server. 

Instructions
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
    
#### Install dependencies

To install dependencies, run

    pip install -r requirements.txt
    
License
-------

Octo-SFTP is licensed under the [MIT License](LICENSE).