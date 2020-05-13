import socket
from collections import ChainMap
from typing import Dict, List

from .custom_types import DiscoveryData, SocketConnection


class Scanner:
    def __init__(self, discovery_timeout: int = 2, search_target: str = 'roku:ecp'):
        self.discovery_timeout: int = discovery_timeout
        self.discovered_devices: list = []
        self.search_target: str = search_target

    def discover(self) -> List[DiscoveryData]:
        ssdp_message: str = f'M-SEARCH * HTTP/1.1\r\n' \
                            f'HOST:239.255.255.250:1900\r\n' \
                            f'ST:{self.search_target}\r\n' \
                            f'MX:2\r\n' \
                            f'MAN:"ssdp:discover"\r\n' \
                            f'\r\n' \

        socket_connection: SocketConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        socket_connection.settimeout(self.discovery_timeout)
        socket_connection.sendto(bytes(ssdp_message, 'utf8'), ('239.255.255.250', 1900))

        try:
            while True:
                d, a = socket_connection.recvfrom(65507)
                address: tuple = a
                data: bytes = d
                device_data: DiscoveryData = self.parse_data(data=data)
                device_data.update({
                    'address': {
                        'host': address[0],
                        'port': address[1]
                    }
                })
                self.discovered_devices.append(device_data)
        except socket.timeout:
            pass

        socket_connection.close()

        return self.discovered_devices

    def parse_data(self, data: bytes) -> Dict[str, str]:
        decoded_data: str = data.decode('utf8')
        header_list: list = decoded_data.split('\n')
        formatted_headers = [self.header_str_to_header_dict(header_str=header_str) for header_str in header_list[1:-2]]

        return dict(ChainMap(*formatted_headers))

    @staticmethod
    def header_str_to_header_dict(header_str: str) -> Dict[str, str]:
        key, value = header_str.split(':', 1)
        return {key: value.strip()}
