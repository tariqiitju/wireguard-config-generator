import logging as log
from os.path import exists
class Config:
    # init method or constructor
    server_private_key_location = '/etc/wireguard/private.key'

    def __init__(self, **data):
        if 'private_key_path' in data:
            x = data['private_key_path']
            if x == None or len(x) == 0:
                log.error('server private key path should not be null or empty')
                exit(-1)
            self.server_private_key_location = x
            if not exists(self.server_private_key_location):
                log.error('Server private key does not exist')
                exit(-1)
            self.server_private_key = open(self.server_private_key_location)
            log.debug(self.server_private_key)


