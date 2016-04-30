
from tendo import singleton
from OctoSFTP import OctoSFTP

if __name__ == '__main__':

    # Check to make sure only a single instance is running
    instance = singleton.SingleInstance()

    # Program execution
    octosftp = OctoSFTP()

    try:
        octosftp.run()
    except KeyboardInterrupt:
        print("Exiting...")
