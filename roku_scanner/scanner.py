# coding=utf-8
import socket
from collections import ChainMap
from typing import Dict, List

from .custom_types import DiscoveryData, SocketConnection


class Scanner:
    """
    Handles device discovery and socket connection data parsing.

    *Attributes:
        discovery_timeout (int): Timeout for each device's discovery ping return.
        discovered_devices (list[DiscoveryData]): List of any discovered devices data.
        search_target (str): Determines whether M:Search will search for only Roku or any device UPnP capable. See Note

    *Note:
        only rokus: roku:ecp
        all devices: upnp:rootdevice
    """
    def __init__(self, discovery_timeout: int = 2, search_target: str = 'roku:ecp'):
        self.discovery_timeout: int = discovery_timeout
        self.discovered_devices: list = []
        self.search_target: str = search_target

    def discover(self) -> List[DiscoveryData]:
        """
        Sets up socket connection for SSDP discovery and handles formatting responses into a list of DiscoveryData

        *Returns:
            list[DiscoveryData] : A list of any discovered devices data
        """
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
                raw_data: tuple = socket_connection.recvfrom(65507)
                data: bytes = raw_data[0]
                device_data: DiscoveryData = self.parse_data(data=data)
                self.discovered_devices.append(device_data)
        except socket.timeout:
            pass

        socket_connection.close()

        return self.discovered_devices

    def parse_data(self, data: bytes) -> Dict[str, str]:
        """
        Parses raw byte data from socket connection headers into a dictionary. Does not add connection status code,
        line 1 data example.

        *Args:
            data (bytes): raw bytes data from connection

        *Returns:
            dict (str, str)

        *Example:
            input:
                b'HTTP/1.1 200 OK\r\n
                Cache-Control: max-age=3600\r\n
                ST: roku:ecp\r\n
                USN: uuid:roku:ecp:YN00XF7876856\r\n
                Ext:\r\n
                Server: Roku/9.2.0 UPnP/1.0 Roku/9.2.0\r\n
                LOCATION: http://127.0.0.1:8060/\r\n
                device-group.roku.com: DD45456B11E45456E51\r\n
                WAKEUP: MAC=e6-48-b0-c7-42-5c;Timeout=10\r\n
                \r\n
                \r\n'
            output: {
                'Cache-Control': 'max-age=3600',
                'ST': 'roku:ecp',
                'USN': 'uuid:roku:ecp:YN00XF7876856',
                'Ext': '',
                'Server': 'Roku/9.2.0 UPnP/1.0 Roku/9.2.0'
                'LOCATION': 'http://127.0.0.1:8060/'
                'device-group.roku.com': 'DD45456B11E45456E51'
                'WAKEUP': 'MAC=e6-48-b0-c7-42-5c;Timeout=10'
            }
        """
        decoded_data: str = data.decode('utf8')
        header_list: list = decoded_data.split('\n')
        formatted_headers = [self.header_str_to_header_dict(header_str=header_str) for header_str in header_list[1:-2]]

        return dict(ChainMap(*formatted_headers))

    @staticmethod
    def header_str_to_header_dict(header_str: str) -> Dict[str, str]:
        """
        Formats socket connection header into a dictionary split at the :.

        *Args:
            header_str (str): header from connection response

        *Returns:
            dict (str, str): dictionary from header str
        """
        key, value = header_str.split(':', 1)
        return {key: value.strip()}
