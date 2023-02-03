
import logging, os, socket

from utils.config import Config



client_config_sample = '''
[Interface]
PrivateKey = __CLIENT_PRIVATE_KEY
Address = 172.25.0.2/16
Address = fd80:f8c3:1783::2/64
[Peer]
PublicKey = __SERVER_PUBLIC_KEY
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = vpn.tariq.com.bd:51820
'''


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)

    if os.getuid() != 0:
        logging.error("You need root previlage perform this operation. try running again as sudo")
        exit(-2)
    q = Config()
