
from OctoSFTP import OctoSFTP

if __name__ == '__main__':
    octosftp = OctoSFTP()

    try:
        octosftp.run()
    except KeyboardInterrupt:
        print("Exiting...")