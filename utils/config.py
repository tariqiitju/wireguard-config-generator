import logging as log
from os.path import exists
import subprocess, ipaddress, socket


class Config:
    # init method or constructor
    server_configuration_file_location = '/etc/wireguard/wg0.conf'
    ipv4Start = None
    ipv4End = None
    ipv6Start = None
    ipv6End = None
    server_port = None
    server_private_key = None
    server_address = None
    def __init__(self, **data):
        log.debug('Initializing configuration file')
        if 'confPath' in data:
            x = data['confPath']
            if x == None or len(x) == 0:
                log.error('server configuration file path should not be null or empty')
                exit(-1)
            self.server_configuration_file_location = x
            if not exists(self.server_configuration_file_location):
                log.error('Server configuration file does not exist')
                exit(-1)
        log.debug('server configuration file path {}'.format(self.server_configuration_file_location))

        interfaceStart = False
        interfaceEnd = False

        for line in open(self.server_configuration_file_location).readlines():
            # print(line)
            if interfaceEnd:
                break
            if line.strip() == '[Interface]':
                interfaceStart  = True
                continue
            lineData = line.strip()
            if lineData == '':
                continue
            if lineData[0] =='[' and lineData[-1] == ']':
                if interfaceStart:
                    interfaceEnd = True
                continue
            if interfaceStart and not interfaceEnd:
                keyEndLocation = lineData.find('=')
                key = lineData[:keyEndLocation].strip()
                value = lineData[keyEndLocation+1:].strip()
                # print(key, value)
                if key == 'PrivateKey':
                    self.server_private_key = value
                elif key == 'ListenPort':
                    self.server_port = int(value)
                elif key == 'Address':
                    subnetList = value.split(',')
                    ipv4Found = False
                    ipv6Found =False
                    for subnet in subnetList:
                        net = ipaddress.ip_network(subnet.strip())
                        if net.version == 4:
                            if ipv4Found:
                                log.error("Invalid network address configuraion. Mutiple ipv4 network")
                                exit(-5)
                            ipv4Found  = True
                            startAddress = int(net[0]) + 2
                            endAddress  = int(net[-1])
                            self.ipv4Start = startAddress
                            self.ipv4End = endAddress
                        elif net.version == 6:
                            if ipv6Found:
                                log.error("Invalid network address configuraion. Mutiple ipv6 network")
                                exit(-5)                                
                            ipv6Found = True
                            startAddress  = int(net[0]) + 2
                            endAddress  = int(net[-1])
                            self.ipv6Start = startAddress
                            self.ipv6End = endAddress

            



        log.debug(self.server_private_key)
        # generate public key from private key
        # system(self.server_private_key + ' | wg pubkey')
        if self.server_private_key[-1]=='\n':
            self.server_private_key = self.server_private_key[:-1]
        cmd = 'echo "' + self.server_private_key + '" | wg pubkey'
        log.debug('Generating public key with {}'.format(cmd))
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        self.server_public_key = str(result.stdout)
        if self.server_public_key[0] == 'b' and \
            self.server_public_key[1] == "'" and \
                self.server_public_key[-1] == "'":
                self.server_public_key = self.server_public_key[2:-1]
        
        if self.server_public_key[-1] == 'n' and self.server_public_key[-2] == '\\':
            self.server_public_key = self.server_public_key[:-2]
        if self.server_public_key[-1] == '\n':
            self.server_public_key = self.server_public_key[:-1]

        log.debug('Server public key: {}'.format(self.server_public_key))
        if 'serverAddess' in data:
            try:
                ip =  ipaddress.ip_address(data["serverAddess"])
                if ip.version == 4:
                    self.server_address = str(ip)
                elif ip.version == 6:
                    self.server_address = '[' + str(ip) + ']'
            except ValueError as e:
                self.server_address = data['serverAddess'].strip()

        if self.server_address == None:
            log.warn("Server address not provided. Atempting to collect from system")
            hostname=socket.gethostname()   
            ipAddr=socket.gethostbyname(hostname) 
            self.server_address = str(ipAddr)
        log.info('Server address: ' + self.server_address)

