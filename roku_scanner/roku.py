# coding=utf-8
import asyncio
import json
import requests
import xmltodict  # type: ignore

from typing import Dict, Union

from .custom_types import DiscoveryData, EcpData, Response, Task


class Roku:
    """
    Gets detailed device information and handles formatting.

    *Attributes:
        location (str): Location(ip) to Roku device. Comes from location header during discovery.
        discovery_data (DiscoveryData): Device discovery data. See custom_types
        data (dict): Fetched data from ECP requests.
    """
    def __init__(self, location: str, discovery_data: DiscoveryData):
        self.location: str = location
        self.discovery_data: DiscoveryData = discovery_data
        self.data: dict = {}

    def fetch_data(self) -> None:
        """
        Intermediary function to request further device data from fetch_all_data()
        """
        self.data = asyncio.run(fetch_all_data(self.location))

    def as_json(self, exclude: Union[list, None] = None) -> str:
        """
        Formats device data into JSON.
        """
        device_name: str = 'unknown-device'
        try:
            device_name = self.data["device_info"]["data"]["device-info"]["default-device-name"]
        except KeyError:
            pass

        temp: dict = {}

        for data_set in self.data.items():
            data: Union[dict, None] = None
            if exclude is not None:
                if data_set[0] not in exclude:
                    data = data_set[1].get('data', None)
            else:
                data = data_set[1].get('data', None)

            if data is not None:
                temp.update(data_set[1]['data'])

        return json.dumps({device_name: temp})

    def as_xml(self, exclude: Union[list, None] = None) -> str:
        """
        Formats device data into XML.
        """
        device_name: str = 'unknown-device'
        try:
            device_name = self.data["device_info"]["data"]["device-info"]["default-device-name"]
        except KeyError:
            pass

        temp: str = f'<{device_name}>\n'

        for data_set in self.data.items():
            xml: Union[dict, None] = None
            if exclude is not None:
                if data_set[0] not in exclude:
                    xml = data_set[1].get('xml', None)
            else:
                xml = data_set[1].get('xml', None)

            if xml is not None:
                temp += data_set[1]['xml'].replace('<?xml version="1.0" encoding="UTF-8" ?>', '')

        temp += f'</{device_name}>\n'

        return temp


async def fetch_all_data(roku_location: str) -> dict:
    """
    Create async tasks for requesting more data from device.

    *Args:
        roku_location (str): IP address to device.

    *Returns (dict): {
        'device_info': data from {roku_location}:8060/query/device-info
        'apps': data from {roku_location}:8060/query/apps,
        'active_app': data from {roku_location}:8060/query/active-app,
        'media_player': data from {roku_location}:8060/query/media-player
    }

    *Note:
        Roku ECP
        https://developer.roku.com/docs/developer-program/debugging/external-control-api.md
    """
    device_info: Task = asyncio.create_task(fetch_device_info(roku_location))
    apps: Task = asyncio.create_task(fetch_apps(roku_location))
    active_app: Task = asyncio.create_task(fetch_active_app(roku_location))
    media_player: Task = asyncio.create_task(fetch_media_player(roku_location))

    return {
        'device_info': await device_info,
        'apps': await apps,
        'active_app': await active_app,
        'media_player': await media_player
    }


async def fetch_device_info(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for device info following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): device data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/device-info', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        device_data_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': device_data_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_apps(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for apps following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): app data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/apps', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        apps_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': apps_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_active_app(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for active-app following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): active-app data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/active-app', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        active_app_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': active_app_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_media_player(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for media player following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): media player data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/media-player', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        media_player_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': media_player_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}
