import logging

from utils.config import Config


if __name__ == '__main__':
    # Creating different objects
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)

    q = Config(private_key_path = '../README.md')

